# use LAMMPS with GPU

#!/bin/bash -l
#
#SBATCH --job-name="-gpu"
#SBATCH --time=24:00:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread
#SBATCH --constraint=gpu
#SBATCH --account=s1183
#========================================
# load modules and run simulation
module load daint-gpu
module load LAMMPS/23Jun2022-CrayGNU-21.09-cuda
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export NO_STOP_MESSAGE=1
export CRAY_CUDA_MPS=1 # to 
ulimit -s unlimited

echo "start MD..."

srun lmp_mpi -sf gpu -in in.lammps
