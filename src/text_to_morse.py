#! /usr/bin/env python

"""
text_to_morse

Creates morse audio file from corresponding text
"""
import logging
import os

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")

# Text to morse dictionary
text_dict = {'A': '.-',     'B': '-...',   'C': '-.-.',
             'D': '-..',    'E': '.',      'F': '..-.',
             'G': '--.',    'H': '....',   'I': '..',
             'J': '.---',   'K': '-.-',    'L': '.-..',
             'M': '--',     'N': '-.',     'O': '---',
             'P': '.--.',   'Q': '--.-',   'R': '.-.',
             'S': '...',    'T': '-',      'U': '..-',
             'V': '...-',   'W': '.--',    'X': '-..-',
             'Y': '-.--',   'Z': '--..',
             '0': '-----',  '1': '.----',  '2': '..---',
             '3': '...--',  '4': '....-',  '5': '.....',
             '6': '-....',  '7': '--...',  '8': '---..',
             '9': '----.'
             }


def to_morse(msg):
    keys = text_dict.keys()
    morse_code = ""
    for c in msg:
        c = c.upper()
        if c == ' ':
            morse_code += '\t'
        if c in keys:
            morse_code += text_dict[c] + " "
    return morse_code


def text2audio(input_file, output_file, samples_dir):
    text = open(input_file, "r").read()
    text = text.upper()
    logger.debug(text)

    try:
        os.remove(output_file)
    except OSError:
        pass

    audio = open(output_file, "ab")
    logger.debug(audio)

    silence_unit = open(samples_dir + "silence_unit.mp3", mode="rb").read()
    for c in text:
        if c == ' ':
            for i in range(4):  # Space is 7 silence units but 3 are contained at the start and end of characters' files
                audio.write(silence_unit)
        elif c in text_dict.keys():
            with open(samples_dir + c + "_morse_code.mp3", mode="rb") as sample:
                sample = sample.read()
                audio.write(sample)

    # Append some silence units at the end
    for i in range(10):
        audio.write(silence_unit)



def main():
    import argparse

    parser = argparse.ArgumentParser(description="Creates morse audio file from corresponding text")
    parser.add_argument("--input", "-i", required=True, help="File containing the text to encode")
    parser.add_argument("--output", "-o", required=False, default="output.mp3", help="Resulting mp3 file")
    parser.add_argument("--samples", required=False, default="../assets/samples/", help="Samples directory")

    args = parser.parse_args()

    text2audio(args.input, args.output, args.samples)


if __name__ == "__main__":
    main()
