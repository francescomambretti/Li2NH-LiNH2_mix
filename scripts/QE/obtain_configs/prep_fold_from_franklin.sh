# written by Francesco Mambretti
# creates the desired (empty) folders for the data to be copied from Franklin to here
# 18/01/2022
#!/bin/bash

#params
main_folder="/scratch/snx3000/fmambret/lithium_amide_imide/256_atoms"
frank_origin="/work/fmambretti/lithium_imide_amide/256_atoms"
list_conc=(0_NH2_750K 12_NH2_750K  16_NH2_750K  4_NH2_750K  8_NH2_750K)
nruns=3

#make folders
cd $main_folder

for i in ${list_conc[*]}; do
	mkdir -p $main_folder/$i
	for (( j=0; j<$nruns; j++ )); do
		mkdir -p $main_folder/$i/run_$j
	done
done
