# written by Francesco Mambretti
# creates the desired (empty) folders for the data to be copied from Franklin to here
# 04/04/2023

main_folder=/work/fmambretti/lithium_imide_amide/MD/384_surface/round2/750K_equil_by_steps
list_conc=(24_NH2)
destination=/scratch/snx3000/fmambret/Li_NH_NH2/QE/384_surface/round2

nruns=3

for i in ${list_conc[*]}; do
    for (( j=1; j<$nruns; j++ )); do
			echo $i,$j	
			nohup scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' $main_folder/$i/run_$j/dump/ fmambret@daint.cscs.ch:$destination/$i/run_$j/
			nohup scp -r -o 'ProxyCommand ssh fmambret@ela.cscs.ch nc %h %p' $main_folder/$i/run_$j/model_devi.out fmambret@daint.cscs.ch:$destination/$i/run_$j/
    done
done
