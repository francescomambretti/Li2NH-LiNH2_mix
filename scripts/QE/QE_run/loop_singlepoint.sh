# written by Francesco Mambretti
# 20/01/2023

folders=(12_NH2_750K  16_NH2_750K  4_NH2_750K  8_NH2_750K)

for f in ${folders[*]}; do
	cd $f
	pwd
	for i in 0 1 2; do
		cp ../0_NH2_750K/run_0/sbatch_cscs.sh run_$i/
		cd run_$i/
		sbatch sbatch_cscs.sh
		cd ..
	done
	cd ..
done
