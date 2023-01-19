# LithiumImiAmi
software for Lithium Imide/Amide solid solutions: simulations and analysis

- `script` folder:
--> `anal_output_LAMMPS`: scripts to analyze/plot output from LAMMPS MD simulations, like plotting model deviations

--> `gen_conf_for_LAMMPS`: generate new configurations for LAMMPS, adding new H atoms to create amides

--> `QE_to_NN`: take the .out files from Quantum Espresso simulations and extract from them the relevant info for the Neural Network (using DeepMD format)

--> `sel_conf_for_QE`: select MD configurations to give them to QE, according to their deviations & create respective QE input files
