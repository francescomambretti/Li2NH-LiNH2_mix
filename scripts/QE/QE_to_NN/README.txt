Scripts in this folder transform QE outputs in inputs for DeepMD.

- 'loop_QE_to_NN.sh' launches 'QE_to_NN.sh' over a set of folders; it extracts the relevant info from QE *.out files and creates the *.raw files.

- 'loop_raw_to_set.sh' works on the same folders, generating the set.*** files (usually only one) from the *raw files.

There is also a (work in progress) trial to do separate analysis for training and validation (but, to date, there are issues with DeepMD NN training).
