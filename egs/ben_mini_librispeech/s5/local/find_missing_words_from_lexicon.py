#! /usr/bin/env python3


""""""

from __future__ import unicode_literals

import io
from argparse import ArgumentParser


stdout = io.open(1, mode="wt", encoding="utf-8", closefd=False)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--train-test-vocab",
        dest="train_test_vocab",
        required=True,
        help="input file containing vocab from train and test set",
        metavar="FILE",
    )

    parser.add_argument(
        "--google-vocab",
        dest="google_vocab",
        required=True,
        help="input file containing vocab from google",
        metavar="FILE",
    )

    args = parser.parse_args()

    train_test_words = []
    with open(args.train_test_vocab, encoding='utf8') as train_test_vocab_file:
        for line in train_test_vocab_file:
            train_test_words.append(line.strip())

    missing_words = []
    with open(args.google_vocab, encoding='utf8') as google_vocab_file:
        for line in google_vocab_file:
            if line.strip() not in train_test_words:
                missing_words.append(line.strip())
    
    for word in missing_words:
        stdout.write(word + "\n")


if __name__ == "__main__":
    main()
