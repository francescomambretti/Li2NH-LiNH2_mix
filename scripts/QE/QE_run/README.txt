Scripts in this folder are used to launch QE calculations.

- `loop_singlepoint.sh` loops over a set of folders, launching inside each one the (SLURM/PBS) script `scf_job_*.sh` for pw.x execution

- `scf_job_*.sh` executes pw.x; if "rm -rf ./tmp" is commented, the data necessary to wave functions (and also charges, and other) computation are deleted. Uncomment it only in case you want to use also pp.x afterwards.

Ideal protocol:
0) select configurations
1) `bash loop_singlepoint.sh` on the desired folders (without removing tmp folders if needed)

If needed:
2) `bash wavefunc_extractor.sh` (analysis) --> obtain HOMO/LUMO indexes
3) `sbatch sbatch_pp.sh` to obtain .cube files, e.g. for visualization with VESTA/VMD (to be adapted for PBS). The script is in the `pp_analysis` folder.

REMINDER: always do benchmarking for your problem on a new computer
REMINDER #2: adapt script names inside files

The 'multi' versions of the scripts for step 1) are meant to simultaneously execute the code on a number of subfolders, named like QE1, QE2, QE3, ... This is useful when a single folder contains a lot of single points to do, and the total time of the computation would overcome the maximum time limit.