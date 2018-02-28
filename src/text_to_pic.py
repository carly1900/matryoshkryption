#!/usr/bin/env python

"""
text_to_pic.py

Creates a picture containing the text given as input
"""
import argparse
import logging
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile
from PIL import ImageFont
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")


def create_picture(input_file, output_file, width=600, height=200):
    text = open(input_file, "r").read()

    pic = Image.new("RGB", (600, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype("/usr/share/fonts/TTF/Inconsolata-Bold.ttf", 32)
    w, h = draw.textsize(text, font=font)
    draw.text(((width - w) // 2, (height - h) // 2), text, (0, 0, 0), font=font)

    pic.show()
    pic.save(output_file)


def main():
    parser = argparse.ArgumentParser(description="Creates a picture containing the text given as input")
    parser.add_argument("--input", "-i", required=True, help="File containing the text")
    parser.add_argument("--output", "-o", required=False, default="text.png", help="Output file")

    args = parser.parse_args()
    logger.debug(args)

    create_picture(args.input, args.output)


if __name__ == "__main__":
    main()
