# written by Francesco Mambretti
# creates the desired (empty) folders for the data to be copied from Daint to here
# 18/01/2022
#!/bin/bash

main_folder=/work/fmambretti/lithium_imide_amide/NN/adding_256_with_NH2 #local folder
list_conc=("0_NH2_750K" "12_NH2_750K"  "16_NH2_750K"  "4_NH2_750K"  "8_NH2_750K")
source=/scratch/snx3000/fmambret/lithium_amide_imide/256_atoms/ #source folder on pizdaint

for i in ${list_conc[*]}; do
	mkdir -p $main_folder/$i/
	nohup scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' fmambret@daint.cscs.ch:$source/$i/*raw $main_folder/$i/ &
	nohup scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' fmambret@daint.cscs.ch:$source/$i/set.000/ $main_folder/$i/ &
done
