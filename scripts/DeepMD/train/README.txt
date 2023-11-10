Edit the relevant parameters inside `auto_prepare_input.sh` to create separate folders for each trained NN. This script launches many copies of sub-*.sh, to run the different jobs. Scripts are - so far - conceived for running the NN training on Franklin @IIT.

`input_template.json` is a template JSON file (remember: no comments!). 
Parameters that can be changed: "decay_steps", "stop_batch". 

Hand-rule: 
batch_size= --> can be chosen
n_gpus=4 (can be changed, however)
n_epochs=int(tot_data/(batch_size*n_gpus))
decay_step=const*n_epochs
n_steps=200*decay_step

`sub-multi_gpu.sh` is the most used (ok for train, train with restart, freeze and compress)

N.B.: to determine `sel`, follow the [instructions here] (https://docs.deepmodeling.com/projects/deepmd/en/master/model/sel.html)

`plot_lcurve.py`: plots the desired info (on a png file) from `lcurve.out`