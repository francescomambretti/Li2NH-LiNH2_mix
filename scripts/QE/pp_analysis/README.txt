- Here, `sel_conf_COLVAR_and_devi.py` is special, since it also provides for creating a separate tmp_$i file for  each selected configuration, so to have distinguished folders for further pp.x execution.
It works exactly as `sel_conf_COLVAR_and_devi.py` in case of pure pw.x execution, concerning all the other features.

Before running the following, pw.x needs to be executed (usually, through the `loop_singlepoint.sh` and `scf_job_*.sh` scripts contained in the `QE_run` folder.

- `sbatch_pp.sh` does pp.x execution over each single tmp_* folder (so it requires naming tmp_$i the $i-th folder yet during pw.x execution). Here, the loop is inside the script.
The `ntmp` parameter has to be explicitly set inside the script. Number of nodes, tasks per node, cpus per task etc. can be optimized.

- `pp.inp` is a prototype for pp.x execution (N.B. 1 --> give to it the right tmp_$i data; 2 --> find the right band indexes with `wavefunc_extractor.sh` and `homo_lumo.py`, see `QE_analysis` folder). From it, a pp.$i.inp file is obtained for every frame.
N.B.: kband(1) and kband(2) numbering starts from 1 and they are both included

- the `template.in` used here is special only in that it takes into account the specific tmp_$i folder. 
