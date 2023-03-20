myfile="./12_NH2/config0.xyz"

awk < $myfile 'BEGIN {ORS=","} {if ($1=="H") print NR}' >H_idxs.dat
awk < $myfile 'BEGIN {ORS=","} {if ($1=="N") print NR}' >N_idxs.dat
awk < $myfile 'BEGIN {ORS=","} {if ($1=="Li") print NR}' >Li_idxs.dat
