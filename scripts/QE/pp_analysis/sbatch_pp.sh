#!/bin/bash -l
#
#SBATCH --job-name="qe-gpu"
#SBATCH --time=06:00:00
#SBATCH --nodes=1
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

echo "start running pp..."

ntmp=50

for i in $( eval echo {0..$ntmp} ); do
	echo $i
	sed "s/\$i/$i/g" pp.inp > pp.$i.inp
	srun pp.x -in pp.$i.inp > tmp_$i/pp.out
	rm pp.$i.inp
done
