# written by Francesco Mambretti
# creates the desired (empty) folders for the data to be copied from Franklin to here
# 18/01/2022
#!/bin/bash

#function scp_to_daint(){
#    scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' "$1" fmambret@daint.cscs.ch:"$2"
#}

main_folder=/work/fmambretti/lithium_imide_amide/256_atoms #here
#list_conc=(16_NH2_750K)
list_conc=(0_NH2_750K 12_NH2_750K  16_NH2_750K  4_NH2_750K  8_NH2_750K)
destination=/scratch/snx3000/fmambret/lithium_amide_imide/MD/256_atoms/ #dest folder on pizdaint
nruns=3

for i in ${list_conc[*]}; do
    for (( j=0; j<$nruns; j++ )); do
			echo $i,$j
			nohup scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' $main_folder/$i/run_$j/dump/ fmambret@daint.cscs.ch:$destination/$i/run_$j/
			nohup scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' $main_folder/$i/run_$j/model_devi.out fmambret@daint.cscs.ch:$destination/$i/run_$j/
    done
done
