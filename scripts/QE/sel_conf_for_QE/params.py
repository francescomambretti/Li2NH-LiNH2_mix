# written by Francesco Mambretti
# 28/04/2023

# classify the LAMMPS configurations according to the model deviations
sigma_list=[0.15,0.2,0.3,0.5]

# files and folders
main_folder="../../"
start=0
end=2 #included
file_devi_name="model_devi.out"
template_QE="template_Li2NH_NH2.in"
num_lin_from_template_QE=38 #cat these many lines from the template
dir_QE_files="QE/"
QE_rootname="scf"
natoms=384

#other params
dump_start=0
dump_freq=1
