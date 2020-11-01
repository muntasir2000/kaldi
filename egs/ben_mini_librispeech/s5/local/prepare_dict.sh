#!/usr/bin/env bash

# if [ $# -ne "1" ]; then
#   echo "Usage: $0 <g2p-dir>"
#   echo "e.g.: $0  data/local/g2p_model"
#   exit 1
# fi

g2p_dir=data/local/g2p_model

mkdir -p $g2p_dir

set -o errexit
set -o nounset
export LC_ALL=C

stage=2
. utils/parse_options.sh || exit 1
. ./path.sh || exit 1

lexicon_tsv_file_url=https://raw.githubusercontent.com/google/language-resources/master/bn/data/lexicon.tsv
dict_clean=data/local/g2p/lexicon_google.txt

mkdir -p data/local/g2p

if [ $stage -le 0 ]; then
    echo "Downloading tsv file from github."
    wget -O data/local/g2p/lexicon.tsv $lexicon_tsv_file_url
    cat data/local/g2p/lexicon.tsv | local/kaldi_lexicon_from_tsv.py > $dict_clean
fi


if [ $stage -le 1 ]; then
    echo "Training G2P model"
    echo "Skipping g2p model training."
    steps/dict/train_g2p.sh --iters 4 $dict_clean $g2p_dir
fi


if [ $stage -le 2 ]; then
    echo "Creating other files"

    full_lexicon=data/local/dict_nosp/lexicon.txt
    nonsilence_phones=data/local/dict_nosp/nonsilence_phones.txt

    mkdir -p data/local/dict_nosp
    
    awk '{for (i = 2; i <= NF; ++i) print $i}' data/train/text data/test/text |
    sort -u > data/local/dict_nosp/vocabulary_train_test.txt
    
    awk '{print $1}' "$dict_clean" |
    sort -u > data/local/dict_nosp/vocabulary_google_lex.txt
    
    # find out which words are present in our train+test set, but not in google lexicon
    local/find_missing_words_from_lexicon.py --train-test-vocab data/local/dict_nosp/vocabulary_train_test.txt \
          --google-vocab data/local/dict_nosp/vocabulary_google_lex.txt > data/local/dict_nosp/missing_words.txt
    
    steps/dict/apply_g2p.sh data/local/dict_nosp/missing_words.txt $g2p_dir data/local/dict_nosp/oov_lex

    echo "Finished generating pronunciations for missing words."

    # Add silence word and phone to lexicon
    echo "!SIL  sil" > "$full_lexicon"
    echo "<UNK> spn" >> "$full_lexicon"

    # combine lexicons
    
    # remove pronunciation probabilities from oov lex
    local/remove_pron_probs_from_lexicon.py < data/local/dict_nosp/oov_lex/lexicon.lex \
    > data/local/dict_nosp/oov_lex/lexicon_no_prob.lex 

    cat $dict_clean data/local/dict_nosp/oov_lex/lexicon_no_prob.lex | sort | uniq >> $full_lexicon

    echo "Final word count in lexicon:  $(cat $full_lexicon | awk '{print $1}' | wc -l)" 
    
    awk '{for (i = 3; i <= NF; ++i) print $i}' "$full_lexicon" | sort -u > "$nonsilence_phones"
    
    
    
    # Creating empty files and silence only files
    echo "sil" > data/local/dict_nosp/silence_phones.txt
    echo "spn" >> data/local/dict_nosp/silence_phones.txt

    echo "sil" > data/local/dict_nosp/optional_silence.txt
    touch data/local/dict_nosp/extra_questions.txt
    
fi


# if [ $stage -le 3 ]; then
#     echo "Training G2P model"
    
# fi