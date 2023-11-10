# written by Francesco Mambretti
# 22/09/2023

#folders=(20NH2_lay11) #(10NH2_lay11  10NH2_lay22  20NH2_lay11  20NH2_lay22)
#main=/scratch/snx3000/fmambret/Li_NH_NH2/QE/384_surface/bias_NN_pair_wNH3_r4/

folders=(20_NH2)
main=/scratch/snx3000/fmambret/Li_NH_NH2/QE/384_surface/round5_postNH3/

cwd=$(pwd)

for f in ${folders[*]}; do
	#cd ${main}/$f/pace250_bias200
	cd ${main}/$f/
	pwd
	for i in {2..2}; do
			for j in {0..10}; do
		    cp ${cwd}/sbatch_scf_multi.sh run_$i/sbatch_scf_multi_$j.sh
		    cd run_$i/
		    sbatch sbatch_scf_multi_$j.sh $j
		    cd ..
			done
	done
	cd ../..
done
