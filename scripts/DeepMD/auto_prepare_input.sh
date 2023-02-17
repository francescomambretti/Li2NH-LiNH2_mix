#Original code by Manyi Yang
#Modified by Francesco Mambretti, 24/01/2023

templateinput='input_template-4GPU-with_NH2.json' #'./input_template-4GPU-with_NH2.json'  #'./input_template-4GPU-francesco.json'
dirs='tr-1 tr-2' 
#'tr-1 tr-2' 
#'tr-all-2 tr-all-3 tr-all-4' # add-upto-12NH2-2 add-upto-12NH2-3 add-upto-12NH2-4' 

root_dir="./4GPU-bs4/" #"./4GPU-bs4/" #"new_raw"
i=0

for dir in $dirs #do 4 random copies
do
	i=$(($i+1))
  mkdir -p $root_dir/$dir
  seed1=$RANDOM
  seed2=$RANDOM
  seed3=$RANDOM
  cp $templateinput $root_dir/$dir/input.json
  sed -i 's/SEED1/'"$seed1"'/' $root_dir/$dir/input.json
  sed -i 's/SEED2/'"$seed2"'/' $root_dir/$dir/input.json
  sed -i 's/SEED3/'"$seed3"'/' $root_dir/$dir/input.json
  cd $root_dir/$dir
  #cp ../../sub-one_gpu.sh . #sub-multi_gpu.sh .
	#qsub sub-one_gpu.sh
	cp ../../sub-multi_gpu.sh .
	qsub sub-multi_gpu.sh
  cd ../..
done
