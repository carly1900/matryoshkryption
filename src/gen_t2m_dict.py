#!/usr/bin/env python

"""
generate_t2m_dict

Creates a python dictionary associating characters to music notes
that can later be used to produce a music score with Lilypond.
"""
import itertools
import json
import random
import sys


def gen_dict(output_file):
    l = list(map(' '.join, itertools.product("abcdefg", repeat=4)))
    random.shuffle(l)

    d = dict(zip([chr(i) for i in range(128)], l))

    f = open(output_file, 'w')
    f.write(json.dumps(d))


def main():
    if len(sys.argv) == 2:
        output_file = sys.argv[1]
    else:
        output_file = "t2m_dict"

    gen_dict(output_file)


if __name__ == "__main__":
    main()
