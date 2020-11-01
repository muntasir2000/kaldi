#! /bin/bash

# Copyright 2018 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ ! -d "$1" ] ; then
  echo >&2 "Usage: prep.sh CORPUSDIR"
  exit 1
fi

set -o errexit
set -o nounset
export LC_ALL=C

readonly CORPUSDIR="$1"

#
# Kaldi recipe directory layout
#

# Create the directories needed
mkdir -p data/local/dict data/local/tmp data/train data/test

# Symlink path setup file expected to be present in the recipe directory
# ln -sf ../common/path.sh

# Symlink auxiliary Kaldi recipe subdirectories
# kaldi_egs_dir="$KALDI_ROOT/egs"
# ln -sf "$kaldi_egs_dir/wsj/s5/steps"
# ln -sf "$kaldi_egs_dir/wsj/s5/utils"
# ln -sf "$kaldi_egs_dir/rm/s5/local"
# ln -sf "$kaldi_egs_dir/rm/s5/conf"

#
# Training and test data
#
tsv_dir=data/local/tsv_files
mkdir -p $tsv_dir

full_file=$tsv_dir/utt_spk_text.tsv
train_file=$tsv_dir/utt_spk_text-train.tsv
test_file=$tsv_dir/utt_spk_text-test.tsv

# Symlink the corpus info file and perform a train/test split
ln -sf "$CORPUSDIR/utt_spk_text.tsv" "$full_file"
local/traintest-split.sh "$full_file" $tsv_dir

echo "Preparing training data, this may take a while"
local/kaldi_converter.py -d $CORPUSDIR -f $train_file --alsent > data/train/al_sent.txt
local/kaldi_converter.py -d $CORPUSDIR -f $train_file --spk2utt    | sort -k1,1 > data/train/spk2utt
local/kaldi_converter.py -d $CORPUSDIR -f $train_file --spk2gender | sort -k1,1 > data/train/spk2gender
local/kaldi_converter.py -d $CORPUSDIR -f $train_file --text       | sort -k1,1 > data/train/text
local/kaldi_converter.py -d $CORPUSDIR -f $train_file --utt2spk    | sort -k1,1 > data/train/utt2spk
local/kaldi_converter.py -d $CORPUSDIR -f $train_file --wavscp     | sort -k1,1 > data/train/wav.scp
echo "Training data prepared"

echo "Preparing test data, this may take a while"
local/kaldi_converter.py -d $CORPUSDIR -f $test_file  --alsent > data/test/al_sent.txt
local/kaldi_converter.py -d $CORPUSDIR -f $test_file  --spk2utt    | sort -k1,1 > data/test/spk2utt
local/kaldi_converter.py -d $CORPUSDIR -f $test_file  --spk2gender | sort -k1,1 > data/test/spk2gender
local/kaldi_converter.py -d $CORPUSDIR -f $test_file  --text       | sort -k1,1 > data/test/text
local/kaldi_converter.py -d $CORPUSDIR -f $test_file  --utt2spk    | sort -k1,1 > data/test/utt2spk
local/kaldi_converter.py -d $CORPUSDIR -f $test_file  --wavscp     | sort -k1,1 > data/test/wav.scp
echo "Test data prepared"

# clean and normalize train and test text files
cat data/train/text | local/clean_and_normalize_text.py > data/train/text.cleaned
rm data/train/text 
mv data/train/text.cleaned data/train/text

cat data/test/text | local/clean_and_normalize_text.py > data/test/text.cleaned
rm data/test/text 
mv data/test/text.cleaned data/test/text


# Fix sorting issues etc.
utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/test
