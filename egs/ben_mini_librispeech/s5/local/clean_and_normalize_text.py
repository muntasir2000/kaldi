#! /usr/bin/env python3

"""
"""

from __future__ import unicode_literals

import io
import re
import string

from bn_num2word import Num2WordBn


STDIN = io.open(0, mode='rt', encoding='utf-8', closefd=False)
STDOUT = io.open(1, mode='wt', encoding='utf-8', closefd=False)


number_pattern = re.compile('[0-9]+')
num2word = Num2WordBn()


def clean_text(text):
    if type(text) is not str:
        print('error: {}'.format(text))
        return ''
    cleaned_text = re.sub(r'[^\u0980-\u09FF ]', ' ', text)
    cleaned_text = cleaned_text.strip(string.punctuation+'\n')
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text


def normalize_numbers_to_words(text):

    text = re.sub('০','0',text)
    text = re.sub('১','1',text)
    text = re.sub('২','2',text)
    text = re.sub('৩','3',text)
    text = re.sub('৪','4',text)
    text = re.sub('৫','5',text)
    text = re.sub('৬','6',text)
    text = re.sub('৭','7',text)
    text = re.sub('৮','8',text)
    text = re.sub('৯','9',text)
    
    matches = number_pattern.findall(text)
    for match in matches:
        print(match)
        word = num2word.num_to_word(match)
        text = re.sub(match, word, text)

    return text
    

def main():

  for line in STDIN:
    line = line.rstrip('\n')
    parts = line.split(" ")

    utt_id = parts[0]
    transcript = " ".join(parts[1:])

    if len(transcript) == 0:
        print("Ignoring empty transcript for utterence.") 
        continue

    cleaned_transcript = clean_text(transcript)
    normalized_transcript = normalize_numbers_to_words(cleaned_transcript)
    
    STDOUT.write('%s %s\n' % (utt_id, normalized_transcript))
    
  return


if __name__ == '__main__':
  main()