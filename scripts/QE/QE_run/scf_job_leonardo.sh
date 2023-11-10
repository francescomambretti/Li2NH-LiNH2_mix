#!/bin/bash -l
#
#SBATCH --job-name="qe-run384"
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --account=IIT23_AtomSim_0
#SBATCH --partition boost_usr_prod
#========================================
# load modules and run simulation
module load profile/chem-phys
module load quantum-espresso/7.2--openmpi--4.1.4--gcc--11.3.0-openblas
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export NO_STOP_MESSAGE=1
export CRAY_CUDA_MPS=1
ulimit -s unlimited

echo "start running QE..."

for name in `ls -v QE/scf*.in`
  do
    prefix=${name%.in}
    srun pw.x -in ${prefix}.in > ${prefix}.out
    rm -rf ./tmp
  done
