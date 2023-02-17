# Written by Francesco Mambretti, 06/02/2023

folders=("0_NH2_750K" "12_NH2_750K" "16_NH2_750K" "4_NH2_750" "8_NH2_750K")

for f in ${folders[*]}; do
    mkdir -p ../256_atoms/$f/train
    mkdir -p ../256_atoms/$f/valid
    
	sh QE_to_NN.sh ../256_atoms/$f/ 2
done
