
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

if [ $# -ne 2 ]; then
  echo "Usage: $0 <DOWNLOAD_DIR> <UNZIP_DIR>"
  echo "e.g.: $0 /storage/dataset/downloads /storage/dataset/extracted"
fi

for d in 0 1 2 3 4 5 6 7 8 9 a b c d e f; 
do
  echo $d
  resource="asr_bengali_${d}.zip"
  # wget -P $1 "http://www.openslr.org/resources/$resource"
  # zipfile="$1/$(basename "$resource")"
  zipfile="$1/$resource"
  unzip -nqq "$zipfile" -d $2
  # rm -f "$1/$zipfile"
done

