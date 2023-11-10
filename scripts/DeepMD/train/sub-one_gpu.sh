#!/bin/bash -l
#PBS -l select=1:ncpus=2:mpiprocs=1:ngpus=1:ompthreads=1
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -q gpu

source /projects/atomisticsimulations/Manyi/Miniconda3-DeepMD-2.1-test.env

cd $PBS_O_WORKDIR

if [ ! -f tag_0_finished ] ;then  #if the file tag_0_finished exists, check the (possible) presence of checkpoints (for restart)
  { if [ ! -f model.ckpt.index ]; then CUDA_VISIBLE_DEVICES=0 horovodrun -np 1 dp train --mpi-log=master input.json; else CUDA_VISIBLE_DEVICES=0 horovodrun -np 1  dp train --mpi-log=master input.json --restart model.ckpt; fi }  1>> train.log 2>> train.log 
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
