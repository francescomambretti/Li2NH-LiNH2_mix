# Li2NH-LiNH2_mix
scripts for the investigation of Ammonia decomposition on Lithium Imide/Amide solid solutions. 
(https://pubs.acs.org/doi/10.1021/acscatal.3c05376)

- `scripts` folder content:
    ->`QE`: run single-point calculations and wavefunction calculations
    ->`DeepMD`: scripts for NN training
    -> `LAMMPS`: scripts for generating initial configurations, creating custom mixtures, running LAMMPS simulations and analyzing the output
    
- `QE`:
1) `obtain_configs` --> copy dump files and other relevant files (such as model deviations and colvar files) in the current computer
2) `sel_conf_for_QE` --> select a subset of configurations for scf calculations
3) `QE_run` --> run Quantum Espresso calculations
4)  `pp_analysis` -->  (optional): run wavefunction calculation (for visualization)
5) `QE_analysis` --> plot distribution of computed energies, analyze wavefunctions, etc.
6) `QE_to_NN` --> convert QE outputs in \*.raw and set.\*\*\* files

-`DeepMD`:
1) `train` --> scripts for training Neural Network potentials with DeepMD-Kit (https://github.com/deepmodeling/deepmd-kit)
2) `dp-test` --> contains a bash script to run `dp test` on a set of subfolders

-`LAMMPS`:
1) `ìnit_configs` --> collection of initial configurations (in LAMMPS dump format) used in simulations + scripts to generate them. ASE (https://wiki.fysik.dtu.dk/ase/) is required to generate some of the initial configurations with the provided notebooks. 
2) `run_LAMMPS` --> script to run LAMMPS on a cluster + LAMMPS input scripts for: bulk, surface, surface + ammonia
3)  `plumed_LAMMPS` --> contains plumed & plumed driver scripts to be run with LAMMPS
4) `anal_output_LAMMPS` --> script to analyze LAMMPS outputs
