# by Francesco Mambretti, 05/01/2023
# 17/02/2023 version

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

	os.system("cp clean.sh  "+target_folder)
	os.system("cp init_configs/Li2NH_256_"+str(N)+"NH2.lmp "+target_folder)

	s = open("in.lammps").read()
	s = s.replace("$SEED1", format(n1)).replace("$SEED2", format(n2)).replace("$N_", format(N))
	s2 = open("sub_dplmp_franklin.sh").read()
	s2 = s2.replace("$NUMBER", format(i)) 

	f = open(target_folder+"/in.lammps", "w")
	f.write(s)
	f.close()
	f = open(target_folder+"/sub_dplmp_franklin.sh", "w")
	f.write(s2)
	f.close()
	
	os.chdir(target_folder)
	os.system("sh clean.sh")
	os.system("qsub sub_dplmp_franklin.sh")
	os.chdir(current_dir)
