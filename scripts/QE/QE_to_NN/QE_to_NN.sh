# Code written by Manyi Yang
# Modified by Francesco Mambretti, 04/10/2023
# Folder structure: outer folder -> fixed chemical composition
# inner folder -> run_0, run_1, ...
# build one single .raw file inside each outer folder, cumulating data from all the runs
# provide as input 1) the outer folder and 2) the num of runs

#remove previous files, if they exist
#test -f energy.raw && rm energy.raw
#test -f force.raw && rm force.raw
#test -f coord.raw && rm coord.raw
#test -f box.raw && rm box.raw
#test -f virial.raw   && rm virial.raw
#mkdir -p Unfinished
#test -f unfinish.info && rm unfinish.info

#conversion factors 
ry2ev=13.605693009
bohr2ang=0.52917721067
kbar2evperang3=0.0006241509125104129 # this is for virial #1e3/1.602176621e6
NN=0

#folders
outer_folder=$1
min_run=$2
max_run=$3
root_folder=./

type_written=0

#clean
cd $outer_folder
for run in `seq $min_run $max_run`; do
	echo "run_"$run
	cd "run_"$run
	write_folder=$outer_folder/run_$run
	test -f && rm $write_folder/*.raw
	pwd
	for name in `ls -v QE/*.out`
		do
			r=`awk 'BEGIN{srand(); x=rand(); print x}'`
			finished=$( grep 'JOB DONE.' $name| wc -l )
			notconverged=$( grep 'convergence NOT achieved' $name| wc -l )
			if [[ $finished != 1 || $notconverged>0 ]] 
			then
				echo $name >> unfinish.info
				mv $name Unfinished
				continue
			else # job has converged
				grep '!    total energy              =' $name |awk 'BEGIN{a='"$ry2ev"'}{printf "%.8f\n",$5*a }' >> $write_folder/energy.raw
				NN=$((NN+1))
			fi
			
			natom=$(grep 'number of atoms/cell      =         ' $name |awk '{print $5}')
			n1=$(echo| awk "{print $natom+1}")
			n2=$(echo| awk "{print $natom+2}")
			alat=$(grep 'celldm(1)=  ' $name| awk -v a="$bohr2ang" '{printf "%.5f",$2*a}')
			cell_a1=$(grep 'a(1) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$4*a}')
			cell_a2=$(grep 'a(1) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$5*a}')
			cell_a3=$(grep 'a(1) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$6*a}')
			cell_b1=$(grep 'a(2) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$4*a}')
			cell_b2=$(grep 'a(2) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$5*a}')
			cell_b3=$(grep 'a(2) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$6*a}')
			cell_c1=$(grep 'a(3) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$4*a}')
			cell_c2=$(grep 'a(3) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$5*a}')
			cell_c3=$(grep 'a(3) = ' $name| awk 'BEGIN{a='"$alat"'}{printf "%.5f",$6*a}')
			echo "$cell_a1 $cell_a2 $cell_a3 $cell_b1 $cell_b2 $cell_b3 $cell_c1 $cell_c2 $cell_c3" >> $write_folder/box.raw
			vol=$(echo| awk "{print $cell_a1*$cell_b2*$cell_c3}")
			f_convert=$(echo| awk "{print $ry2ev/$bohr2ang}")
			grep -A $n1 'Forces acting on atoms (cartesian axes, Ry/au):' $name | tail -n $natom | awk 'BEGIN{a='"$f_convert"'}{printf("%.10f %.10f %.10f ", $7*a,$8*a,$9*a)} END {printf ("\n")}' >> $write_folder/force.raw

			grep -A $n2 'Cartesian axes' $name | tail -n $natom | awk 'BEGIN{a='"$alat"'} {printf ("%.5f %.5f %.5f ",$7*a,$8*a,$9*a)} END {printf ("\n")}' >> $write_folder/coord.raw
			grep -A 3 'total   stress' $name |tail -n 3 | awk 'BEGIN{a='"$kbar2evperang3"';b='"$vol"'}{printf ("%.8f %.8f %.8f ",$4*a*b,$5*a*b,$6*a*b)} END {printf ("\n")}' >> $write_folder/virial.raw
			if [ $type_written -eq 0 ]
			then
      	  grep -A $n1 'Forces acting on atoms' $name |tail -n $natom | awk '{printf ("%i \n",$4-1 )}' >> $write_folder/type.raw
    	    echo 'H N Li' > $write_folder/type_map.raw
  	      type_written=1
			fi
		done
		cd ..
done

#mv type*raw ./

cd $root_folder
