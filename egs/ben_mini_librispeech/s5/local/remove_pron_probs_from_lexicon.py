#! /usr/bin/env python3

"""Converts a pronunciation lexicon in TSV format to Kaldi lexicon format.
"""

from __future__ import unicode_literals

import io
import re


STDIN = io.open(0, mode="rt", encoding="utf-8", closefd=False)
STDOUT = io.open(1, mode="wt", encoding="utf-8", closefd=False)



def main(unused_args):

    for line in STDIN:
        line = line.rstrip("\n")
        
        fields = line.split("\t")
        assert len(fields) >= 3

        word = fields[0]
        pronunciation = fields[2]

        STDOUT.write("%s %s \n" % (word, pronunciation))

    return


if __name__ == "__main__":
    main(None)
