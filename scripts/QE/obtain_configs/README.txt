Get configurations, usually (but not mandatory) as .xyz files, as well as all the other files necessary for running QE calculations.

`copy_from_MD.sh` creates folders and copies files within the same machine (MD to QE folder).

`prep_fold_from_franklin.sh` creates the right folders on the local machine, based on MD trajectories present on a remote machine.

`scp_all_to_daint.sh` is located where the MD has been done, e.g. on Franklin; its purpose is to copy all the dump files onto the machine were QE will be run, e.g. Piz Daint.