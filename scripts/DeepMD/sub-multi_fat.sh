#!/bin/bash -l
#PBS -l select=1:ncpus=20:mpiprocs=4:ngpus=4:ompthreads=5
#PBS -l walltime=72:00:00
#PBS -j oe
#PBS -q fat

source /projects/atomisticsimulations/Manyi/Miniconda3-DeepMD-2.1-test.env

cd $PBS_O_WORKDIR

if [ ! -f tag_0_finished ] ;then  
	CUDA_VISIBLE_DEVICES=0,1,2,3 horovodrun -np 4  dp train --mpi-log=master input.json 1>> train.log 2>> train.log
  if test $? -ne 0; then touch tag_failure_0; fi 
fi

if [ ! -f tag_1_finished ] ;then #training is over, freeze the model
  dp freeze  1>> train.log 2>> train.log 
  touch tag_1_finished 
fi

if [ ! -f tag_2_finished ] ;then #compress the model
  dp compress   1>> train.log 2>> train.log 
  touch tag_2_finished 
fi
