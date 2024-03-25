# Written by Francesco Mambretti
# 19/04/2023

ext_folder=$1
maxrun=$2
curr_folder=$pwd

cd $ext_folder

for r in `seq 0 $maxrun`; do
	cd run_$r
	ls -v msd_H_*.dat | xargs tail -q -n +3 > msd_H.dat
	ls -v msd_N_*.dat | xargs tail -q -n +3 > msd_N.dat
	ls -v msd_NH_*.dat | xargs tail -q -n +3 > msd_NH.dat
	ls -v msd_Li_*.dat | xargs tail -q -n +3 > msd_Li.dat
	cd ..
done

cd $curr_folder
