chain_sub_dplmp_franklin.bias.surf.sh --> run chained jobs with a single GPU
run-dplmp-franklin-multi-time-walks.sh --> does the same on many GPUs (with usage of "world" variables in LAMMPS
sub_dplmp_franklin.sh --> run simple job (no automatic restart)
sbatch_cscs.sh --> does the same on CSCS cluster

Such scripts are iteratively called through loop*py Python scripts (for running replicas)
