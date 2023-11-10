# LithiumImiAmi
scripts for the investigation of Ammonia decomposition on Lithium Imide/Amide solid solutions. 
[preprint] (https://chemrxiv.org/engage/chemrxiv/article-details/654b646b2c3c11ed71f64104)

- `script` folder content:
    -`QE`: run single-point calculations and wavefunction calculations
    -`DeepMD`: scripts for NN training
    - `LAMMPS`: scripts for generating initial configurations, creating custom mixtures, running LAMMPS simulations and analyzing the output
    
- `QE`:
1) `obtain_configs` --> copy dump files and other relevant files (such as model deviations and colvar files) in the current computer
2) `sel_conf_for_QE` --> select a subset of configurations for scf calculations
3) `QE_run` --> run Quantum Espresso calculations
4)  `pp_analysis` -->  (optional): run wavefunction calculation (for visualization)
5) `QE_analysis` --> plot distribution of computed energies, analyze wavefunctions, etc.
6) `QE_to_NN` --> convert QE outputs in \*.raw and set.\*\*\* files
