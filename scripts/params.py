# written by Francesco Mambretti
# 12/01/2023

# classify the LAMMPS configurations according to the model deviations
sigma_1=0.025
sigma_2=0.035
sigma_3=0.045
sigma_4=0.065

# files and folders
folder_sim="../256_atoms/0_NH2_750K/run_0/"
file_devi_name="model_devi.out"
template_QE="template_Li2NH_NH2.in"
num_lin_from_template_QE=39
dir_QE_files="QE_in/"
QE_rootname="scf"

#other params
dump_start=400000 #equilibration steps -> maybe, do timestep reset in LAMMPS
dump_freq=2000
