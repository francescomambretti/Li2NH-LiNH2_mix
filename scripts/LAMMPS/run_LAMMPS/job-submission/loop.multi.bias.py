# by Francesco Mambretti, 05/01/2023
# 20/09/2023 version

import random
import os
import sys

if (len(sys.argv) < 7):
    print("Error! please provide the folder, the bias, the pace, the idxs of the start/end runs (end included) and the number of NH2 molecules")
    sys.exit(-1)

#cmd line args
folder=sys.argv[1]
bias=sys.argv[2]
pace=sys.argv[3]
start=int(sys.argv[4])
end=int(sys.argv[5])
N=sys.argv[6] #number of NH2

replicas=4 #to be used with world variables in LAMMPS

dump_freq=80 #plumed
folder=folder+"/pace"+pace+"_bias"+bias
os.system("mkdir -p "+folder)

random.seed(8922)

current_dir=os.getcwd()

layers_pairs_10_1=[389,220,389,218]
layers_pairs_10_2=[256,259,257,226]
layers_pairs_20_1=[385,385,260,226]
layers_pairs_20_2=[61,248,261,181]

atoms_dic_1={"10": layers_pairs_10_1, "20": layers_pairs_20_1}
atoms_dic_2={"10": layers_pairs_10_2, "20": layers_pairs_20_2}

try:    
    os.mkdir(folder)
except:
    pass

for i in range (start,end+1):

    n10 = random.randint(0,10000)
    n11 = random.randint(0,10000)
    n12 = random.randint(0,10000)
    n13 = random.randint(0,10000)
    n20 = random.randint(0,10000)
    n21 = random.randint(0,10000)
    n22 = random.randint(0,10000)
    n23 = random.randint(0,10000)  
	
    target_folder=folder+"/run_{}".format(i)
    print(target_folder)

    try:	
        os.mkdir(target_folder)
    except:
        pass

    #create list of H,N,Li indexes
    os.system("sh awk_sel_idxs.sh init_configs/equi.surface384_"+str(N)+"NH2_2NH3.deprot."+str(i)+".lmp idxs_folder")

    with open("idxs_folder/N_idxs.dat","r") as fileread:
        nlist=fileread.read()
    with open("idxs_folder/H_idxs.dat","r") as fileread:
        hlist=fileread.read()
    with open("idxs_folder/Li_idxs.dat","r") as fileread:
        lilist=fileread.read()

    os.system("cp init_configs/equi.surface384_"+str(N)+"NH2_2NH3.deprot.*.lmp "+target_folder)
    os.system("cp ../bck.meup.sh "+target_folder)

    for j in range (0,replicas):
        os.system("cp plumed.dat "+target_folder+"/plumed."+str(j)+".dat")

    s = open("in.bias.multi.lammps").read()
    s = s.replace("$SEED1_0", format(n10)).replace("$SEED1_1", format(n11)).replace("$SEED1_2", format(n12)).replace("$SEED1_3", format(n13)).replace("$SEED2_0", format(n20)).replace("$SEED2_1", format(n21)).replace("$SEED2_2", format(n22)).replace("$SEED2_3", format(n23)).replace("$N_", format(N))
    s2 = open("run-dplmp-franklin-multi-time-walks.sh").read()
    s2 = s2.replace("$NUMBER", format(i)).replace("$N_", format(N)) 

    f = open(target_folder+"/in.bias.multi.lammps", "w")
    f.write(s)
    f.close()
    f = open(target_folder+"/run-dplmp-franklin-multi-time-walks.sh", "w")
    f.write(s2)
    f.close()

    for j in range (0,replicas):
        a1 = atoms_dic_1[str(N)][j]
        a2 = atoms_dic_2[str(N)][j]
        s3 = open("plumed.dat").read()
        s3 = s3.replace("$HLIST", format(hlist)).replace("$NLIST", format(nlist)).replace("$LILIST", format (lilist)).replace("$BIAS",format(bias)).replace("V_DUMP",format(dump_freq)).replace("$PACE",format(pace)).replace("$ATOM1", format(a1)).replace("$ATOM2", format(a2))
        f = open(target_folder+"/plumed."+str(j)+".dat", "w")
        f.write(s3)
        f.close()

    os.chdir(target_folder)
    os.system("qsub run-dplmp-franklin-multi-time-walks.sh")
    os.chdir(current_dir)
