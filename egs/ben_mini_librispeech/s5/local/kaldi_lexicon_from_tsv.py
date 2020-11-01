#! /usr/bin/env python

"""Converts a pronunciation lexicon in TSV format to Kaldi lexicon format.
"""

from __future__ import unicode_literals

import io
import re


STDIN = io.open(0, mode="rt", encoding="utf-8", closefd=False)
STDOUT = io.open(1, mode="wt", encoding="utf-8", closefd=False)

english_pattern = re.compile("[A-Za-z0-9]+")


def main(unused_args):

    for line in STDIN:
        line = line.rstrip("\n")
        # Skip comments
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        assert len(fields) >= 2

        word = fields[0]
        pronunciation = fields[1]

        if english_pattern.match(word):
            # some words in the lexicon are english, skip them
            continue

        phones = [p for p in pronunciation.split(" ") if p != "."]
        phones_str = " ".join(phones)

        STDOUT.write("%s %s \n" % (word, phones_str))

    return


if __name__ == "__main__":
    main(None)
