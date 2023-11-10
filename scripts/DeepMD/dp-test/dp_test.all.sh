#!/bin/bash -l
#PBS -l select=1:ncpus=2:mpiprocs=2:ngpus=1:ompthreads=1
#PBS -l walltime=00:15:00
#PBS -j oe
#PBS -q debug

source /projects/atomisticsimulations/Manyi/Miniconda3-DeepMD-2.1-test.env

cd $PBS_O_WORKDIR

main_f=256_bulk #384_surf_post  #bias_NN
#subfolders=(10NH2_lay11  10NH2_lay22  20NH2_lay11  20NH2_lay22)
subfolders=(0_NH2 16_NH2) #10_NH2 20_NH2)
runs=(0 1 2 3)

for sf in ${subfolders[*]}; do
	for r in ${runs[*]}; do
		dp test -m /work/fmambretti/lithium_imide_amide/NN/round4_train/1GPU-bs8-a100/tr-1/frozen_model_compressed.pb  -s ./$main_f/$sf/run_$r -n 50000 -d tr-1_$main_f-$sf-run_$r
	done
done
