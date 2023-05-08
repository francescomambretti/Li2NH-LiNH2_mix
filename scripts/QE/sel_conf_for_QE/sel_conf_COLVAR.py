# by Francesco Mambretti
# select configurations based upon the COLVAR value
# then, prepare input folders for Quantum Espresso
# works looping on replicas, at fixed T and chemical composition of the system
# 05/04/2023 version

import numpy as np
from params import *
import sys
import os
import random

##########################
# loop over replicas

if len(sys.argv)<4:
    print("Set, at least, COLVAR filename and CV min/max values")
    sys.exit(-1)
else:
    colvar_filename=sys.argv[1]
    col_min=float(sys.argv[2])
    col_max=float(sys.argv[3])
    
for r in range (start,end+1):
    selected=[] #list of selected configs
    counter_sel=0

    folder_sim=main_folder+"/run_{}/".format(int(r))

    file=folder_sim+colvar_filename
    steps,CV=np.loadtxt(file,unpack=True,usecols=(0,1,))
    
    print("Working with {} configurations".format(len(steps)))
    
    steps_to_delete=np.zeros(0,dtype=int)
    
    #loop over the configurations, keeping or discarding them based on their CV value
    for i,s in enumerate(CV):
        if (CV[i]>= col_min and CV[i]<=col_max): #transition region
            selected.append(i)
            counter_sel+=1
        else:
            #remove that step
            steps_to_delete=np.append(steps_to_delete,int(i))

    steps=np.delete(steps,steps_to_delete)
            
    print("We are keeping {} configurations".format(counter_sel))

    # send to Quantum Espresso the selected configurations

    # make the directory
    if not os.path.exists(folder_sim+dir_QE_files):
        os.makedirs(folder_sim+dir_QE_files)
        
    for i,config in enumerate(selected): #config is unused, so far

        dump_step=int(steps[int(i)])

        # first part: copy and paste from template
        outname=QE_rootname+"."+str(i)+".in"
        os.system("head -n "+str(num_lin_from_template_QE)+" "+template_QE+" > "+folder_sim+dir_QE_files+outname)

        # second: copy and paste from single LAMMPS configurations
        begin=int((natoms+2)*i)+3 #skip first 2 lines of each frame
        end=int((natoms+2)*(i+1))
        os.system("sed -n "+str(begin)+","+str(end)+"p "+folder_sim+"/dump/dump.xyz >>"+folder_sim+dir_QE_files+outname)
#        os.system("tail -n +3  "+folder_sim+"/dump/dump."+str(dump_step)+".xyz >> "+folder_sim+dir_QE_files+outname)
