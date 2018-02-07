#! /usr/bin/env python3

# AngeCryption: getting valid files after encryption

# takes any file as input, and a standard PDF/PNG/JPG/FLV as target
# will create a result_file that is source_file with appended 'garbage'
# and once ENcrypted with the chosen algorithm with the supplied script, it will show target_file

# any block cipher is supported as long as the block size matches the target type's header

# Ange Albertini 2014, BSD Licence - with the help of Jean-Philippe Aumasson

# Port to Python 3 by L. David

import binascii
import struct
import sys

PNGSIG = b"\x89PNG\r\n\x1a\n"
JPGSIG = b"\xff\xd8"
FLVSIG = b"FLV"

filetype = ""   # useful only to name file when decrypted

source_file, target_file, result_file, encryption_key, algo = sys.argv[1:6]

if algo.lower() == "aes":
    from Crypto.Cipher import AES

    algo = AES
    BLOCKSIZE = 16
else:
    from Crypto.Cipher import DES3  # will work only with JPEG as others require 16 bytes block size

    algo = DES3
    BLOCKSIZE = 8


def pad(pt):
    return pt + (BLOCKSIZE - len(pt) % BLOCKSIZE) * bytes([BLOCKSIZE - len(pt) % BLOCKSIZE])  # non-standard padding might be preferred for PDF


# from Crypto import Random
# key = Random.new().read(16)
key = encryption_key.encode()

with open(source_file, "rb") as f:
    s = pad(f.read())

with open(target_file, "rb") as f:
    t = pad(f.read())

p = s[:BLOCKSIZE]  # our first plaintext block
ecb_dec = algo.new(key, algo.MODE_ECB)

# we need to generate our first cipher block, depending on the target type

if t.startswith(PNGSIG):  # PNG
    assert BLOCKSIZE >= 16
    size = len(s) - BLOCKSIZE
    filetype = "png"

    # our dummy chunk type
    # 4 letters, first letter should be lowercase to be ignored
    chunktype = b"aaaa"

    # PNG signature, chunk size, our dummy chunk type
    c = PNGSIG + struct.pack(">I", size) + chunktype

    c = ecb_dec.decrypt(c)
    #    IV = "".join([chr(ord(c[i]) ^ ord(p[i])) for i in range(BS)]))
    IV = bytes([c[i] ^ p[i] for i in range(BLOCKSIZE)])
    cbc_enc = algo.new(key, algo.MODE_CBC, IV)
    result = cbc_enc.encrypt(s)

    # write the CRC of the remaining of s at the end of our dummy block
    result = result + struct.pack(">I", binascii.crc32(result[12:]) % 0x100000000)
    # and append the actual data of t, skipping the sig
    result = result + t[8:]

elif t.startswith(JPGSIG):  # JPG
    assert BLOCKSIZE >= 2
    filetype = "jpg"

    size = len(s) - BLOCKSIZE  # we could make this shorter, but then could require padding again

    # JPEG Start of Image, COMment segment marker, segment size, padding
    c = JPGSIG + b"\xFF\xFE" + struct.pack(">H", size) + b"\0" * 10

    c = ecb_dec.decrypt(c)
    #    IV = "".join([chr(ord(c[i]) ^ ord(p[i])) for i in range(BS)]))
    IV = bytes([c[i] ^ p[i] for i in range(BLOCKSIZE)])
    cbc_enc = algo.new(key, algo.MODE_CBC, IV)
    result = cbc_enc.encrypt(s)

    # and append the actual data of t, skipping the sig
    result = result + t[2:]
elif t.startswith(FLVSIG):
    assert BLOCKSIZE >= 9
    size = len(s) - BLOCKSIZE  # we could make this shorter, but then could require padding again
    filetype = "flv"

    # reusing FLV's sig and type, data offset, padding
    c = t[:5] + struct.pack(">I", size + 16) + b"\0" * 7

    c = ecb_dec.decrypt(c)
    #    IV = "".join([chr(ord(c[i]) ^ ord(p[i])) for i in range(BS)]))
    IV = bytes([c[i] ^ p[i] for i in range(BLOCKSIZE)])
    cbc_enc = algo.new(key, algo.MODE_CBC, IV)
    result = cbc_enc.encrypt(s)

    # and append the actual data of t, skipping the sig
    result = result + t[9:]
elif t.find(b"%PDF-") > -1:
    assert BLOCKSIZE >= 16
    size = len(s) - BLOCKSIZE  # we take the whole first 16 bits
    filetype = "pdf"

    # truncated signature, dummy stream object start
    c = b"%PDF-\0obj\nstream"

    c = ecb_dec.decrypt(c)
    #    IV = "".join([chr(ord(c[i]) ^ ord(p[i])) for i in range(BS)]))
    IV = bytes([c[i] ^ p[i] for i in range(BLOCKSIZE)])
    cbc_enc = algo.new(key, algo.MODE_CBC, IV)
    result = cbc_enc.encrypt(s)

    # close the dummy object and append the whole t
    # (we don't know where the sig is, we can't skip anything)
    result = result + b"\nendstream\nendobj\n" + t

else:
    print("file type not supported")
    sys.exit()

# we have our result, key and IV

# generate the result file
cbc_dec = algo.new(key, algo.MODE_CBC, IV)
with open(result_file, "wb") as f:
    f.write(cbc_dec.decrypt(pad(result)))

# generate the script
with open("dec-" + target_file + ".py", "w") as ds:
    ds.write(
        """from Crypto.Cipher import %(algo)s

algo = %(algo)s.new(%(key)s, %(algo)s.MODE_CBC, %(IV)s)
with open("%(source)s", "rb") as f:
    d = f.read()
d = algo.encrypt(d)
with open("dec-%(target)s.%(filetype)s", "wb") as f:
    f.write(d)""" % {
            'algo': algo.__name__.split(".")[-1],
            'filetype': filetype,
            'key': key,
            'IV': IV,
            'source': result_file,
            'target': target_file})