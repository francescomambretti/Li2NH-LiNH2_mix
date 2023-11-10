#!/bin/bash -l
#
#SBATCH --job-name="qe-run384"
#SBATCH --time=05:00:00
#SBATCH --nodes=6
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=6
#SBATCH --constraint=gpu
#SBATCH --account=s1183
#========================================
# load modules and run simulation
module load daint-gpu
module load QuantumESPRESSO
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export NO_STOP_MESSAGE=1
export CRAY_CUDA_MPS=1
ulimit -s unlimited

echo "start running QE..."

for name in `ls -v QE$1/scf*.in`
  do
    prefix=${name%.in}
    srun pw.x -in ${prefix}.in > ${prefix}.out
    rm -rf ./tmp
  done
