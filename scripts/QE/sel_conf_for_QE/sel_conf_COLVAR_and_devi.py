# by Francesco Mambretti
# select configurations based upon the COLVAR value
# then, prepare input folders for Quantum Espresso
# works looping on replicas, at fixed T and chemical composition of the system
# 10/11/2023 version

import numpy as np
from params import *
import sys
import os
import random

###################

def assign_to_subgroup(sigma,boundaries): #assign each configuration to a group, based on deviation among the 4 models
    if sigma < boundaries [0]:
        return 0
    elif sigma >= boundaries[0] and sigma < boundaries[1]:
        return 1
    elif sigma >= boundaries[1] and sigma < boundaries[2]:
        return 2
    elif sigma >= boundaries[2] and sigma < boundaries [3]:
        return 3
    else:
        return -1 #means sigma >= boundaries[3] --> discard
        
###################

#set the 4 intervals
boundaries=sigma_list

##########################
# loop over replicas

if len(sys.argv)<5:
    print("Set: COLVAR filename; CV min/max values; file with models deviations")
    sys.exit(-1)
else:
    colvar_filename=sys.argv[1]
    col_min=float(sys.argv[2])
    col_max=float(sys.argv[3])
    file_devi=sys.argv[4]
    
for r in range (start,end+1):
    counter_sel=np.zeros(4,dtype=int)

    folder_sim=main_folder+"/run_{}/".format(int(r))

    #load history of CV values
    fileCV=folder_sim+colvar_filename
    steps,CV=np.loadtxt(fileCV,unpack=True,usecols=(0,1,),skiprows=1)
    
    #load history of model deviations
    file_devi=folder_sim+file_devi_name
    steps,devi=np.loadtxt(file_devi,unpack=True,usecols=(0,4,),skiprows=1+int(dump_start/dump_freq))
    
    if (len(devi)!=len(CV)):
        print("Danger! lengths of CVs and devi array are different")
        print(len(devi),len(CV))
        sys.exit(-1)
    
    print("Working with {} configurations".format(len(steps)))
    
    steps_to_delete=np.zeros(0,dtype=int)
    
    #loop over the configurations, keeping or discarding them based on their sigma (devi)
    for i,s in enumerate(devi):
        subgroup=int(assign_to_subgroup(s,boundaries))
        print(i,s,subgroup,CV[i])
        if (subgroup>=0 and CV[i]>= col_min and CV[i]<=col_max):  #add configuration to selected configurations with a given probability
            if (random.uniform(0, 1)<fractions[subgroup]):
                counter_sel[subgroup]+=1
        else:
            #remove that step
            steps_to_delete=np.append(steps_to_delete,int(i))

    steps=np.delete(steps,steps_to_delete)
            
    print("We are keeping {} configurations".format(counter_sel))

    # send to Quantum Espresso the selected configurations

    # make the directory
    if not os.path.exists(folder_sim+dir_QE_files):
        os.makedirs(folder_sim+dir_QE_files)
        
    for dump_step in steps:

        # first part: copy and paste from template
        outname=QE_rootname+"."+str(i)+".in"
        os.system("head -n "+str(num_lin_from_template_QE)+" "+template_QE+" > "+folder_sim+dir_QE_files+outname)

        # second: copy and paste from single LAMMPS configurations
        begin=int((natoms+2)*i)+3 #skip first 2 lines of each frame
        end=int((natoms+2)*(i+1))
        os.system("sed -n "+str(begin)+","+str(end)+"p "+folder_sim+"/dump/dump.xyz >>"+folder_sim+dir_QE_files+outname)
