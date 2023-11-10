# written by Francesco Mambretti
# creates the desired (empty) folders for the data to be copied here and copies dump files, model_devi etc. (colvar, e.g.) where needed - if the files are located on the same machine
# input args: local path for MD original files (source), local path for QE (destination)
# 10/11/2023

#!/bin/bash

max_id=3

for i in  `eval echo {0..$max_id}`; do
  mkdir -p $2/run_$i/
  cp $1/run_$i/model_devi.out $2/run_$i/
  cp $1/run_$i/dump/dump.xyz $2/run_$i/dump.xyz
done
