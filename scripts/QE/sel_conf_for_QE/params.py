# written by Francesco Mambretti
# 28/04/2023

# classify the LAMMPS configurations according to the model deviations
sigma_list=[0.0503, 0.0560, 0.0610, 0.0685]
fractions=[0.2,0.1,0.05,0.01]

# files and folders
main_folder="/scratch/snx3000/fmambret/Li_NH_NH2/QE/384_surface/round3_withNH3/12_NH2/"
start=0
end=0 #included
file_devi_name="model_devi.out"
template_QE="template_384.surf.in"
num_lin_from_template_QE=38 #cat these many lines from the template
dir_QE_files="QE/"
QE_rootname="scf"
natoms=392

#other params
dump_start=0
dump_freq=1
