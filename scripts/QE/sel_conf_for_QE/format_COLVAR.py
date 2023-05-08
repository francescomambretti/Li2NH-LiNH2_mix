# by Francesco Mambretti
# create a unique COLVAR_ALL file from 2 or more COLVAR files
# shift time & save only CV value
# 28/04/2023 version

import numpy as np
import sys
import os
import random
from params import *

##########################
# input params & settings

if len(sys.argv)<3:
    print("Set number of COLVAR files, time shift factor")
    sys.exit(-1)
else:
    num_files=int(sys.argv[1])
    shift=int(sys.argv[2])
    
for r in range (start,end+1):

    folder_sim=main_folder+"/run_{}/".format(int(r))
    newfile=open(folder_sim+"COLVAR_ALL",'a')

    for n in range(1,1+num_files):
        if n==1:
            file=folder_sim+"COLVAR"
        else:
            file=folder_sim+"COLVAR"+str(n)
            
        steps,CV=np.loadtxt(file,unpack=True,usecols=(0,1,),skiprows=1)
        
        steps-=shift
        np.savetxt(newfile,np.c_[steps,CV])
    newfile.close()
