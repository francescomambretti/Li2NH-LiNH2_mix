# written by Francesco Mambretti
# 20/04/2023

#sys.argv[1] --> external folder for QE files & also save pictures here

#variables
ext_folder=$1  #surface, biased surface, bulk, ... & concentration NH2
max_run=0
suffix="eFermi.dat"

#loop over folders
for run in `seq 0 $max_run`; do
  echo "run_"$run
  mkdir -p $ext_folder/"run_"$run/bands
  Fermifile=$ext_folder/"run_"$run/bands/$suffix
  test -f $Fermifile && rm $Fermifile
  i=0
  for name in `ls -v $ext_folder/run_$run/QE/scf.*.out` #for each frame: extract eigenenergies, subtract E_Fermi and compute HOMO-LUMO Delta Energy
    do
    
    #find Fermi energy and save to a file
    ef=$(grep 'the Fermi energy is     ' $name| awk '{print $5}')
    printf "$ef\n" >> $Fermifile
    
    #now load all the energies and save them into a single-column file
    l1=$(grep -n 'k = 0.0000 0.0000 0.0000 ' $name | cut -d : -f 1)
    l2=$(grep -n 'the Fermi energy is ' $name | cut -d : -f 1)
    
    awk < $name -v l1=$l1 -v l2=$l2 -v ef=$ef '{gsub(/,/,".")}{if (NR>l1+1 && NR<l2-1){ for (i=1; i <= NF; i++) print ($i-ef)}}' > $ext_folder/"run_"$run/bands/bands.$i.dat #print after subtracting the corresponding Fermi energy
    i=$(($i+1))
    done
    
    echo $i
    #compute the HOMO-LUMO Delta Energy & wavefunctions for a few cases
    python homo_lumo.py $ext_folder $i $max_run

done
