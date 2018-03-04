# Matryoshkryption - Solving process


## First Part
* Decompress `matryoshkryption.tar.gz`
* One gets a (malformed) png file (thereafter referred to as `png_file`)

### Handling png file
* Use Gimp to get a proper png, by opening `png_file` and exporting it again to the png format (→ `png_aux.png`)
* Open `png_aux` in stegsolve:
    * Analyse → Data Extract: by ticking only the box corresponding to Bit Plan 0 of the red component, we get a dictionary/alphabet (→ `alphabet.txt`)
    * Using the arrows at the bottom of the window to navigate between the successive components' plans:
        * One finds a key in Green Plan 0 (→ `png_key`)
        * One finds an IV in Blue Plan 0 (→ `png_iv`)  
* The description of the chall leads to understanding that Angecryption was used:
    * use `solve_angecryption.py` to get to the next step:
        `python solve_angecryption.py --input png_file --key png_key --iv png_iv --output png_output`.
    * `> file png_output` → `png_output: PDF document, version .b`
    
    
### Handling pdf file - Part 1
* The content is a music score. One can use the dictionary found previously to decode the notes into actual text.
* One thus gets a message giving a new key (→ `pdf_key`), a new IV (→ `pdf_iv`) and a flag.

__The flag one gets from the music score validates the first part of the challenge__.


## Part 2

### Handling pdf file - Part 2
* The Copyright line of the music score also contains base64-encoded data, which once decoded gives a passphrase (→ `passphrase`).
* De-angecrypt the pdf file with the new key/iv pair: `python solve_angecryption.py --input pdf_file --key pdf_key --iv pdf_iv --output pdf_output`
* `file pdf_output` → `MPEG ADTS, layer III, v1, 128 kbps, 44.1 kHz, Monaural`.
* This is a mp3 file (maybe malformed to some extent).
    
### Handling the mp3 file
* Listening to the mp3 file lets one hear a morse-encoded message and some additional noise.
* Open the file in Audacity: this allows to visualize the sound and decode the morse message more easily.
* One thus gets a new key (→ `mp3_key`).
* Using the Spectrogram view, one also gets a new IV (→ `mp3_iv`).
* De-angecrypt: `python solve_angecryption.py --input mp3_file --key mp3_key --iv mp3_iv --output
mp3_output`
* `> file mp3_output` → `mp3_output: ISO Media, MP4 Base Media v1 [IS0 14496-12:2003]`
* This is a mp4 file.

### Handling the mp4 file
* The video shows nothing particular.
* The passphrase from earlier has not been used yet, it is time to do so.
* The passphrase suggests TrueCrypt has been used. Looking up for "TrueCrypt mp4", one sees that TrueCrypt volumes can be hidden within mp4 ones so that both files are still readable.
* However, TrueCrypt is deprecated and a common alternative for it is VeraCrypt, so let's use VeraCrypt instead: `veracrypt -p passphrase --mount mp4_file <some_mounting_point>`.
* There is a single file in the volume, called `flag`.

__The flag one gets from the eponym file validates the second part of the challenge__.
