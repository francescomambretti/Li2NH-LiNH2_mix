# written by Francesco Mambretti
# 25/04/2023
# 26/04/2023 version

import numpy as np
import os
import matplotlib.pyplot as plt
import sys

#variables
ext_folder=sys.argv[1]
nframes=int(sys.argv[2])
max_run=int(sys.argv[3])

deltas=np.zeros(0)
sel_idxs1=np.zeros(0)
sel_idxs2=np.zeros(0)

#constants
T=750 #K (can be changed)
kB=8.62*1E-5 # Boltzmann constant in (eV / K)

#Fermi-Dirac distribution
def fd (ene,T):
    return 1./(np.exp(ene/(kB*T))+1) #assuming Fermi energy already subtracted

#params for particular configurations selection
sel1=0.2 #eV, small gap
sel2=1.2 #eV, ok gap
toler=0.05
num_chosen=3

for run in range (0,max_run+1): #do it for each run

    #analyze!
    save_folder=ext_folder+"/run_{}/bands".format(run)
    for f in range (0,nframes):
        values=np.loadtxt(ext_folder+"/run_{}/bands/bands.{}.dat".format(run,f))
        index=np.searchsorted(values, 0) #find first positive value, this is LUMO
        deltaE=values[index]-values[index-1] #index-1 is HOMO
        
        if (sel1-toler<= deltaE and deltaE <=sel1+toler): #select special configs
            #print(sel1,f)
            sel_idxs1=np.append(sel_idxs1,f)
            
        elif (sel2-toler<= deltaE and deltaE <=sel2+toler):
            #print(sel2,f)
            sel_idxs2=np.append(sel_idxs2,f)
            
        deltas=np.append(deltas,deltaE) #HOMO-LUMO difference
        
        plt.plot(values,marker='o')
    plt.xlim(index-6,index+5)
    plt.ylim(-3,3)
    plt.savefig(save_folder+"/all_curves.png",dpi=200)

    plt.clf()

    plt.hist(deltas, bins = 30, color='lightseagreen',ec='black')
    plt.xlabel("Gap HOMO-LUMO [eV]")
    plt.ylabel("counts")
    plt.savefig(save_folder+"/counts_gap.png",dpi=200)
    #os.system("open counts_gap.png")

    #now work on the selected configurations
    idxs1=np.random.choice(sel_idxs1,size=num_chosen,replace=False)
    idxs2=np.random.choice(sel_idxs2,size=num_chosen,replace=False)

    f1 = open(save_folder+"/0.2eV_data.txt", "w")
    f2 = open(save_folder+"/1.2eV_data.txt", "w")

    #do also energy spectra plots only for selected frames
    plt.clf()

    for i in idxs1:
        i=int(i)
        values=np.loadtxt(save_folder+"/bands.{}.dat".format(run,i))
        plt.plot(values,marker='o',label="frame {}".format(i))
        for a in range (index-3,index+2): #go from HOMO-2 to LUMO+1 (included)
            pi=fd(values[a],T)
            #print("%d, %d, %.3f 0.2 eV" % (i,a,pi))
            f1.write("%d, %d, %.3f 0.2 eV \n" % (i,a,pi))
            
        #copy chosen frame into 0.2_eV folder
        os.system("cp "+ext_folder+"/run_"+str(run)+"/QE/scf."+str(i)+".in "+ext_folder+"/select/0.2_eV/")

    plt.xlim(index-5,index+5)
    plt.ylim(-3,3)
    plt.legend(loc="lower right")
    plt.savefig(save_folder+"/sel_curves_0.2eV.png",dpi=200)

    plt.clf()

    for i in idxs2:
        i=int(i)
        values=np.loadtxt(save_folder+"/bands.{}.dat".format(run,i))
        plt.plot(values,marker='o',label="frame {}".format(i))
        for a in range (index-3,index+2): #go from HOMO-2 to LUMO+1 (included)
            pi=fd(values[a],T)
            #print("%d, %d, %.3f 1.2 eV" % (i,a,pi))
            f2.write("%d, %d, %.3f 1.2 eV \n" % (i,a,pi))
        
        #copy chosen frame into 1.2_eV folder
        os.system("cp "+ext_folder+"/run_"+str(run)+"/QE/scf."+str(i)+".in "+ext_folder+"/select/1.2_eV/")
            
    plt.xlim(index-6,index+5)
    plt.ylim(-3,3)
    plt.legend(loc="lower right")
    plt.savefig(save_folder+"/sel_curves_1.2eV.png",dpi=200)

    f1.close()
    f2.close()

    ## prepare for pp execution
    path_to_pp_inp=ext_folder+"/select/"
    s = open(path_to_pp_inp+"/pp.inp").read()
    index=index+1 #QE starts from 1, not from 0
    s = s.replace("$K0", format(index-3)).replace("$K1", format(index+2))

    f = open(path_to_pp_inp+"/pp.inp", "w")
    f.write(s)
    f.close()

    print("Now you should run: 1) sbatch sbatch_scf.sh 0.2_eV   2) sbatch sbatch_scf.sh 1.2_eV  3) sbatch sbatch_pp.sh 0.2_eV  4) sbatch sbatch_pp.sh 1.2_eV    inside  the folder: "+ext_folder+"/select/")
