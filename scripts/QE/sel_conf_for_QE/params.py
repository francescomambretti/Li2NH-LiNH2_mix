# written by Francesco Mambretti
# 12/01/2023

# classify the LAMMPS configurations according to the model deviations
sigma_list=[0.15,0.2,0.3,0.5]

# files and folders
main_folder="../../256_atoms/0_NH2_750K/"
nruns=1
file_devi_name="model_devi.out"
template_QE="template_Li2NH_NH2.in"
num_lin_from_template_QE=39
dir_QE_files="QE/"
QE_rootname="scf"

#other params
dump_start=400000 #equilibration steps -> maybe, do timestep reset in LAMMPS
dump_freq=2000
