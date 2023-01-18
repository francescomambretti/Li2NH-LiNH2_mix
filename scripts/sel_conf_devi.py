# by Francesco Mambretti
# select configurations based upon the value of max_devi_f
# then, prepare input folders for Quantum Espresso
# 18/01/2023 version

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

#if (len(sys.argv)<2):
#	print("Error! Too few arguments... provide: ????")
#	sys.exit(-1)

#set the 4 intervals
boundaries=[sigma_1,sigma_2,sigma_3,sigma_4]
fractions=[1,0.9,0.15,0.05] #take this fraction of configurations from each subgroup -> can be changed
selected=[] #list of selected configs
counter_sel=np.zeros(4,dtype=int)

file_devi=folder_sim+file_devi_name
steps,devi=np.loadtxt(file_devi,unpack=True,usecols=(0,4,),skiprows=1+int(dump_start/dump_freq)) #skip equilibration

steps_to_delete=np.zeros(0,dtype=int)

print("Working with {} configurations".format(len(steps)))

#loop over the configurations, keeping or discarding them based on their sigma (devi)

for i,s in enumerate(devi):
    subgroup=int(assign_to_subgroup(s,boundaries))
    if subgroup>=0:
        #add configuration to selected configurations with a given probability
        if (random.uniform(0, 1)<fractions[subgroup]):
            selected.append(i)
            counter_sel[subgroup]+=1
    else:
        #remove that step
        steps_to_delete=np.append(steps_to_delete,int(i))

steps=np.delete(steps,steps_to_delete)
        
print("We are keeping {}, {}, {}, {} in the 4 subgroups respectively, which amounts to a total of {} configurations saved out of {}".format(*counter_sel,np.sum(counter_sel),len(devi)))

# send to Quantum Espresso the selected configurations

# make the directory
if not os.path.exists(folder_sim+dir_QE_files):
    os.makedirs(folder_sim+dir_QE_files)
    
print(steps)

for i,config in enumerate(selected): #config is unused, so far

    dump_step=int(steps[int(i)])

    # first part: copy and paste from template
    outname=QE_rootname+"."+str(i)+".in"
    os.system("head -n "+str(num_lin_from_template_QE)+" "+template_QE+" > "+folder_sim+dir_QE_files+outname)

    # second: copy and paste from single LAMMPS configurations
    os.system("tail +3 "+folder_sim+"/dump/dump."+str(dump_step)+".xyz >> "+folder_sim+dir_QE_files+outname)
