Scripts in this folder are used to launch QE calculations.

- 'loop_singlepoint.sh' loops over a set of folders, launching inside each one the (SLURM/PBS) script 'sbatch_scf.sh' for pw.x execution

- 'sbatch_scf.sh' executes pw.x; if "rm -rf ./tmp" is commented, the data necessary to wave functions (and also charges, and other) computation are deleted. Uncomment it only in case you want to use also pp.x afterwards.
Its actual version is suitable for running on PizDaint (CSCS)

Ideal protocol:
0) select configurations
1) 'bash loop_singlepoint.sh' on the desired folders (without removing tmp folders if needed)

If needed:
2) 'bash wavefunc_extractor.sh' (analysis) --> obtain HOMO/LUMO indexes
3) 'sbatch sbatch_pp.sh' to obtain .cube files, e.g. for visualization with VESTA
