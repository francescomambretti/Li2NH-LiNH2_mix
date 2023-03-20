# by Francesco Mambretti, 05/01/2023
# 20/03/2023 version

import random
import os
import sys

if (len(sys.argv) < 4):
	print("Error! please provide the folder, the number of copies and the number of NH2 molecules")
	sys.exit(-1)

#cmd line args
folder=sys.argv[1]
copies=int(sys.argv[2])
N=sys.argv[3] #number of NH2

bias=200
dump_freq=2000

#create list of H,N,Li indexes
os.system("sh awk_sel_idxs.sh init_configs/Li2NH_384_"+str(N)+"NH2.lmp idxs_folder")

with open("idxs_folder/N_idxs.dat","r") as fileread:
	nlist=fileread.read()
with open("idxs_folder/H_idxs.dat","r") as fileread:
	hlist=fileread.read()
with open("idxs_folder/Li_idxs.dat","r") as fileread:
	lilist=fileread.read()

current_dir=os.getcwd()

random.seed(27893)

for i in range (0,copies):
	n1 = random.randint(0,10000)
	n2 = random.randint(0,10000)

	target_folder=folder+"/run_{}".format(i)
	print(target_folder)

	try:	
		os.mkdir(target_folder)
	except:
		pass

	os.system("cp init_configs/Li2NH_384_"+str(N)+"NH2.lmp "+target_folder)

	s = open("in.bias.surf.lammps").read()
	s = s.replace("$SEED1", format(n1)).replace("$SEED2", format(n2)).replace("$N_", format(N))
	s2 = open("chain_sub_dplmp_franklin.bias.surf.sh").read()
	s2 = s2.replace("$NUMBER", format(i)).replace("$N_", format(N)) 
	s3 = open("plumed.dat").read()
	s3 = s3.replace("$HLIST", format(hlist)).replace("$NLIST", format(nlist)).replace("$LILIST", format (lilist)).replace("$BIAS",format(bias)).replace("V_DUMP",format(dump_freq))

	f = open(target_folder+"/in.bias.surf.lammps", "w")
	f.write(s)
	f.close()
	f = open(target_folder+"/plumed.dat", "w")
	f.write(s3)
	f.close()	
	f = open(target_folder+"/chain_sub_dplmp_franklin.bias.surf.sh", "w")
	f.write(s2)
	f.close()

	os.chdir(target_folder)
	os.system("qsub chain_sub_dplmp_franklin.bias.surf.sh")
	os.chdir(current_dir)
