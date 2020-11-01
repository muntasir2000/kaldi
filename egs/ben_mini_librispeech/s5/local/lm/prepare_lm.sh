#!/usr/bin/env bash

if [ $# -ne "4" ]; then
  echo "Usage: $0 <COMMONCRAWL-DOWNLOAD-DIR> <WORK-DIR> <OUTPUT-DIR> <OUTPUT-ARPA-NAME>"
  echo "e.g.: $0  /data/downloads/commoncrawl_bangla data/local/lm_temp data/local/lm commoncrawl"
  exit 1
fi

downlaod_dir=$1
temp_work_dir=$2
output_dir=$3
arpa_name=$4

mkdir -p $temp_work_dir $output_dir

if [[ -f "$downlaod_dir/bn_part_1.txt.gz" ]]; then
    echo "$downlaod_dir/bn_part_1.txt.gz file doesn't exist. Have you downloaded the deduped texts from CommonCrawl?"
    echo "Please visit https://oscar-corpus.com, register and then download the deduplicated Bangla texts."
fi

# unzip the .gz files 

gzip -cd $downlaod_dir/bn_part_1.txt.gz > $temp_work_dir/bn_part_1.txt  
gzip -cd $downlaod_dir/bn_part_2.txt.gz > $temp_work_dir/bn_part_2.txt
gzip -cd $downlaod_dir/bn_part_3.txt.gz > $temp_work_dir/bn_part_3.txt
gzip -cd $downlaod_dir/bn_part_4.txt.gz > $temp_work_dir/bn_part_4.txt

# clean and normalize text
cat $temp_work_dir/*.txt | local/clean_commoncrawl_bangla_corpus.py > $temp_work_dir/cleaned_combined.txt

# train LM with KenLM
local/lm/train_arpa_with_kenlm.sh $temp_work_dir/cleaned_combined.txt data/lang_nosp/words.txt $output_dir $arpa_name

gzip $output_dir/$arpa_name.arpa 
