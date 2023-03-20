# written by Francesco Mambretti, 12/03/2023

import numpy as np
import ase
from ase.io import read, iread
from ase.io import write
import sys, os

#############################

def load_traj (filename):
    traj = read(filename,index=":", parallel=True)

    return traj

#############################

def info_from_conf(conf,sym1,sym2):
    Ntot=len(conf)
    symbols=conf.get_chemical_symbols()
    N_N=sum(map(lambda x : x==sym1, symbols)) 
    N_Li=sum(map(lambda x : x==sym2, symbols))

    return Ntot,N_N,N_Li

############################

def split_Li_N(atoms,sym1,sym2):

    atoms_Li=ase.Atoms() #create two separate atoms objects
    atoms_N=ase.Atoms()
    for a in atoms:
        if a.symbol==sym1:
            atoms_Li.append(a)
        elif a.symbol==sym2:
            atoms_N.append(a)
    atoms_Li.set_cell(atoms.get_cell())
    atoms_Li.pbc=True
    atoms_N.set_cell(atoms.get_cell())
    atoms_N.pbc=True

    #get indexes
    idx_Li=[atom.index for atom in atoms if atom.symbol == sym1]
    idx_N=[atom.index for atom in atoms if atom.symbol == sym2]
    
    return atoms_Li,atoms_N,idx_Li,idx_N

#############################

def voronoi_analysis(atoms,file1,file2,skip, old_idxs_plus,old_numLi,N_N,offset):
    
    numLi=np.loadtxt(file1,skiprows=skip+offset,max_rows=1)
    idxs_plus=np.loadtxt(file2,skiprows=skip+offset,max_rows=1) #load charge excess data
    
    #detect proton transfers
    if (skip>0):
        if (np.array_equal(idxs_plus,old_idxs_plus)==False):
            iw=np.where(np.array_equal(idxs_plus,old_idxs_plus)==False)
            print(iw) #corresponds to a proton transfer
        #if(np.array_equal(idxs_plus,old_idxs_plus)==False):
        #    print(skip,idxs_plus,old_idxs_plus,)
    
    charge=np.zeros(N_N)
    
    #loop over cells and get their charge
    for c in range (0,N_N):
        if(idxs_plus[c]==0):
            charge[c]=numLi[c]-2 #NH
        else:
            charge[c]=numLi[c]-1 #NH2
    
    old_idxs_plus=np.copy(idxs_plus)
    old_numLi=np.copy(numLi)
    
    return old_idxs_plus,old_numLi,charge

#######################################################################################

### main

traj=load_traj(sys.argv[1])
main_folder="lambda_100"
file1=main_folder+"/NUM_Li.txt"
file2=main_folder+"/INDEXs-PLUS.txt"

box=[14.266,10.187,14.266]

os.system("rm traj_charge.xyz")

for skip,atoms in enumerate(traj[0:1000]): #do the full analysis (without plots)
    if (skip==0):
        Ntot,N_N,N_Li=info_from_conf(atoms,"N","Li") #extract info from config
        
        old_idxs_plus=np.zeros(N_N)
        old_numLi=np.zeros(N_N)
        atoms.set_cell(box)

    #select only Li atoms
    atoms_Li,atoms_N,idx_Li,idx_N=split_Li_N(atoms,"Li","N")
    atoms_Li.set_cell(box)
    atoms_N.set_cell(box)
    
    old_idxs_plus,old_numLi,charge=voronoi_analysis(atoms,file1,file2,skip, old_idxs_plus,old_numLi,N_N,0)

    #write
    atoms_N.set_array('chargeVoro',charge)
    write('traj_charge.xyz',atoms_N,append=True)
