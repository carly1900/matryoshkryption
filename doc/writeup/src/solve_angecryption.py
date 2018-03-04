#!/usr/bin/python

from Crypto.Cipher import AES
import argparse
import logging

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", 
        format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")


def solve(filename, outname, key, iv):
    f_in = open(filename, "rb")
    f_out = open(outname, "wb")
    key = open(key, "rb").read(16)
    iv = open(iv, "rb").read(16)

    logger.debug(key)
    logger.debug(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    indata = f_in.read()
    if len(indata) % 16 == 1:
        indata = indata[0:len(indata)-1]
    print(len(indata))
    out = cipher.decrypt(indata)
    f_out.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt angecrypted file\
            using provided key and iv")
    parser.add_argument("--input", "-i", required=True, help="File to de-angecrypt")
    parser.add_argument("--key", "-k", required=True, help="Key file")
    parser.add_argument("--iv", required=True, help="IV file")
    parser.add_argument("--output", "-o", required=True, help="Output file")

    args = parser.parse_args()
    solve(args.input, args.output, args.key, args.iv)
