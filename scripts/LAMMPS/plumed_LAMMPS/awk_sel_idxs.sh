#this version is OK for lammps dump files
#inside plumed.dat, substitute the explicit list of indexes with $HLIST, $NLIST, $LILIST
myfile="$1"
folder="$2"

awk < $myfile 'BEGIN {ORS=","} {if ($2=="1") print NR}' >$folder/H_idxs.dat
awk < $myfile 'BEGIN {ORS=","} {if ($2=="2") print NR}' >$folder/N_idxs.dat
awk < $myfile 'BEGIN {ORS=","} {if ($2=="3") print NR}' >$folder/Li_idxs.dat
