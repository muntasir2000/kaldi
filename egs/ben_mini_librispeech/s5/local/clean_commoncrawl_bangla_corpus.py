#! /usr/bin/env python3

"""
"""

from __future__ import unicode_literals

import io
import re
import string

from bn_num2word import Num2WordBn


STDIN = io.open(0, mode="rt", encoding="utf-8", closefd=False)
STDOUT = io.open(1, mode="wt", encoding="utf-8", closefd=False)


number_pattern = re.compile("[0-9]+")
split_line_pattern = re.compile("[।?!]")
english_character_pattern = re.compile("[a-zA-Z0-9]+")
brace_pattern = re.compile("[()]")


num2word = Num2WordBn()


def clean_text(text):
    if type(text) is not str:
        return ""
    cleaned_text = re.sub(r"[^\u0980-\u09FF ]", " ", text)
    cleaned_text = cleaned_text.strip(string.punctuation + "\n")
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text


def normalize_numbers_to_words(text):
    text = re.sub("০", "0", text)
    text = re.sub("১", "1", text)
    text = re.sub("২", "2", text)
    text = re.sub("৩", "3", text)
    text = re.sub("৪", "4", text)
    text = re.sub("৫", "5", text)
    text = re.sub("৬", "6", text)
    text = re.sub("৭", "7", text)
    text = re.sub("৮", "8", text)
    text = re.sub("৯", "9", text)

    matches = number_pattern.findall(text)
    for match in matches:
        word = num2word.num_to_word(match)
        text = re.sub(match, word, text)

    return text


def is_valid_sentence(sentence):
    if not isinstance(sentence, str):
        return False

    # filter out too small and too long sentences
    if len(sentence) < 10 or len(sentence) > 150:
        return False

    # filter out sentences containing english characters
    if english_character_pattern.search(sentence):
        return False

    # filter out sentences with braces
    if brace_pattern.search(sentence):
        return False

    # filter out sentences which have : in them (like this শেয়ারবাজার রিপোর্ট:)
    if ":" in sentence:
        return False

    if "ঃ" in sentence:
        return False

    return True


def main():

    for line in STDIN:
        line = line.rstrip("\n")
        sentences = split_line_pattern.split(line)
        for sentence in sentences:
            if not is_valid_sentence(sentence):
                continue
            
            cleaned_transcript = clean_text(sentence)
            normalized_transcript = normalize_numbers_to_words(cleaned_transcript)
            
            STDOUT.write("%s\n" % (normalized_transcript))


if __name__ == "__main__":
    main()
