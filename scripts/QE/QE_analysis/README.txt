Scripts in this folder are used to analyze the outcome of QE execution. 

- 'plot_energy_dist.py' plots an histogram of the energy eigenvalues obtained, for a quick overall check

- 'wavefunc_extractor.sh' is a Bash script which:
	1. Extracts eigenenergies from QE output files
	2. Shifts them around the Fermi energy, producing also a file with all the Fermi energy values for the selected frames (e.g. part of a trajectory)
	3. Saves the energy values in files called bands.$i.dat

- such files are the input for 'homo_lumo.py', which identifies the HOMO-LUMO indexes (usually, it is the same for all the files, if they come from the same system). Moreover, it provides for substituting such values inside the pp.inp file, for the kbands(1) and kbands(2) values.

'homo_lumo_v2.py' works the same as 'homo_lumo.py', but it also produces a plot with the distribution of all the HOMO-LUMO energy gaps (to inspect insulator/conductor behavior), named 'counts_gap.png', together with a zoom on the energy bands of a few selected configurations.
In particular, the version present in this folder analyzes separately some configs with HOMO-LUMO gap close to 0.2 eV, and as many whose gap is ~1.2 eV.
