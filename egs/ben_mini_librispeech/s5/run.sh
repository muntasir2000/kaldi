#!/usr/bin/env bash

# Change this location to somewhere where you want to put the data.
downloaded_data_dir=~/Desktop/google_asr_data
extracted_data_dir=~/Desktop/extracted/google_asr_data_extracted/

mkdir -p $extracted_data_dir

. ./cmd.sh
. ./path.sh

stage=0
. utils/parse_options.sh

set -euo pipefail


# for part in dev-clean-2 train-clean-5; do
#   local/download_and_untar.sh $data $data_url $part
# done



if [ $stage -le 0 ]; then
    # local/download_lm.sh $lm_url $data data/local/lm
    echo "Preparing data. skipping download and extract"
    local/download_data.sh $downloaded_data_dir $extracted_data_dir
    local/data_prep.sh $extracted_data_dir/asr_bengali
    
    # echo "Preparing dict"
    local/prepare_dict.sh
    
    # echo "Preparing lang"
    utils/prepare_lang.sh data/local/dict_nosp \
    "<UNK>" data/local/lang_tmp_nosp data/lang_nosp
    
    echo "Preparing ARPA language model"
    local/lm/prepare_lm.sh /home/tareq/Desktop/datasets/commoncrawl_bangla data/lm_temp_dir data/local/lm "commoncrawl_4gram"

    echo "Formating ARPA language model to FST"
    utils/format_lm.sh data/lang_nosp data/local/lm/commoncrawl_4gram.arpa.gz data/local/dict_nosp/lexicon.txt data/lang_fst 
    
    # Create ConstArpaLm format language model
    utils/build_const_arpa_lm.sh data/local/lm/commoncrawl_4gram.arpa.gz \
    data/lang_nosp data/lang_nosp_test_fglarge
    
fi

# exit 0;


if [ $stage -le 2 ]; then
    mfccdir=mfcc
    
    for part in train test; do
        steps/make_mfcc.sh --cmd "$train_cmd" --nj 10 data/$part exp/make_mfcc/$part $mfccdir
        steps/compute_cmvn_stats.sh data/$part exp/make_mfcc/$part $mfccdir
    done
    
    # Get the shortest 500 utterances first because those are more likely
    # to have accurate alignments.
    utils/subset_data_dir.sh --shortest data/train 500 data/train_500short
fi

# train a monophone system
if [ $stage -le 3 ]; then
    steps/train_mono.sh --boost-silence 1.25 --nj 5 --cmd "$train_cmd" \
    data/train_500short data/lang_nosp exp/mono
    
    # decode using monophone model
    utils/mkgraph.sh data/lang_nosp_test_fglarge exp/mono exp/mono/graph_nosp_tglarge
    steps/decode.sh --nj 5 --cmd $decode_cmd exp/mono/graph_nosp_tglarge \
        data/test exp/mono/decode_nosp_tglarge_test

    steps/align_si.sh --boost-silence 1.25 --nj 5 --cmd "$train_cmd" \
    data/train data/lang_nosp exp/mono exp/mono_ali_train
fi

# train a first delta + delta-delta triphone system on all utterances
if [ $stage -le 4 ]; then
    steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" \
    2000 10000 data/train data/lang_nosp exp/mono_ali_train exp/tri1
    
    steps/align_si.sh --nj 5 --cmd "$train_cmd" \
    data/train data/lang_nosp exp/tri1 exp/tri1_ali_train
fi

# train an LDA+MLLT system.
if [ $stage -le 5 ]; then
    steps/train_lda_mllt.sh --cmd "$train_cmd" \
    --splice-opts "--left-context=3 --right-context=3" 2500 15000 \
    data/train data/lang_nosp exp/tri1_ali_train exp/tri2b
    
    # Align utts using the tri2b model
    steps/align_si.sh  --nj 5 --cmd "$train_cmd" --use-graphs true \
    data/train data/lang_nosp exp/tri2b exp/tri2b_ali_train
fi

# Train tri3b, which is LDA+MLLT+SAT
if [ $stage -le 6 ]; then
    steps/train_sat.sh --cmd "$train_cmd" 2500 15000 \
    data/train data/lang_nosp exp/tri2b_ali_train exp/tri3b
fi

# Now we compute the pronunciation and silence probabilities from training data,
# and re-create the lang directory.
if [ $stage -le 7 ]; then
    steps/get_prons.sh --cmd "$train_cmd" \
    data/train data/lang_nosp exp/tri3b
    utils/dict_dir_add_pronprobs.sh --max-normalize true \
    data/local/dict_nosp \
    exp/tri3b/pron_counts_nowb.txt exp/tri3b/sil_counts_nowb.txt \
    exp/tri3b/pron_bigram_counts_nowb.txt data/local/dict
    
    utils/prepare_lang.sh data/local/dict \
    "<UNK>" data/local/lang_tmp data/lang
    
    local/format_lms.sh --src-dir data/lang data/local/lm
    
    utils/build_const_arpa_lm.sh \
    data/local/lm/commoncrawl_4gram.arpa.gz data/lang data/lang_test_tglarge
    
    steps/align_fmllr.sh --nj 5 --cmd "$train_cmd" \
    data/train data/lang exp/tri3b exp/tri3b_ali_train
fi


if [ $stage -le 8 ]; then
    # Test the tri3b system with the silprobs and pron-probs.
    
    # decode using the tri3b model
    utils/mkgraph.sh data/lang_test_tgsmall \
    exp/tri3b exp/tri3b/graph_tgsmall
    for test in dev_clean_2; do
        steps/decode_fmllr.sh --nj 10 --cmd "$decode_cmd" \
        exp/tri3b/graph_tgsmall data/$test \
        exp/tri3b/decode_tgsmall_$test
        steps/lmrescore.sh --cmd "$decode_cmd" data/lang_test_{tgsmall,tgmed} \
        data/$test exp/tri3b/decode_{tgsmall,tgmed}_$test
        steps/lmrescore_const_arpa.sh \
        --cmd "$decode_cmd" data/lang_test_{tgsmall,tglarge} \
        data/$test exp/tri3b/decode_{tgsmall,tglarge}_$test
    done
fi

# Train a chain model
if [ $stage -le 9 ]; then
    local/chain2/run_tdnn.sh
fi

# local/grammar/simple_demo.sh
