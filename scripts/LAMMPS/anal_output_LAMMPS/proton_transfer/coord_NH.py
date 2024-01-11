# Monitor H transfer among NH2,NH molecules
# using coordination number
# returns a .xyz file
# written by Francesco Mambretti, 02/03/2023
# 16/03/2023 version

import sys
import os
import numpy as np
import ase
from ase.io import read, iread
from ase.io import write
import time as t

if (len(sys.argv)!=3):
    print("Error! 2 arguments needed: traj file, new traj name")

input_file=sys.argv[1]

################################################################################################################
def load_traj (filename):
    traj = read(filename,index=':', parallel=True)
    
    return traj
    
##############################
def info_from_conf(conf,sym1,sym2):
    Ntot=len(conf)
    symbols=conf.get_chemical_symbols()
    N_c=sum(map(lambda x : x==sym1, symbols)) #centers
    N_n=sum(map(lambda x : x==sym2, symbols)) #neighbors

    return Ntot,N_c,N_n
    
##############################
def split_cen_neigh(atoms,sym1,sym2):

    atoms_c=ase.Atoms() #create two separate atoms objects
    atoms_n=ase.Atoms()
    for a in atoms:
        if a.symbol==sym1:
            atoms_c.append(a)
        elif a.symbol==sym2:
            atoms_n.append(a)
    atoms_c.set_cell(atoms.get_cell())
    atoms_c.pbc=True
    atoms_n.set_cell(atoms.get_cell())
    atoms_n.pbc=True

    #get indexes
    idx_c=[atom.index for atom in atoms if atom.symbol == sym1]
    idx_n=[atom.index for atom in atoms if atom.symbol == sym2]
    
    return atoms_c,atoms_n,idx_c,idx_n
    
##############################

def check_rebuild(atoms,idx_c,idx_prev_n,cutoff_build): #decide whether to recompute center-neighbor distances or not

    #loop over center atoms
    ii=0
    for i in idx_c: #compute such distances only for center atoms
        for j in idx_prev_n[ii]:
            r=atoms.get_distance(i,j,mic=True)
            #if (i==108 or i==101):
            #    print(r,j)
            if (r > cutoff_build):
                #print(r)
                return True
            
        ii+=1
        
    return False
    
##############################

def compute_coord(N_c,N_n,atoms_c,atoms_n,idx_c,idx_n,atoms,box,cutoff,rij):

    #get all distances between the selected centers and the selected neighbors
    ii=0
    
    for i in idx_c: #compute such distances only for center atoms
        rij[ii]=(atoms.get_distances(i,idx_n,mic=True)) #get all the distances from neighbors
        ii+=1 #next row
        
    coord_array=np.empty(0)
    
    idx_prev_n=[]
    
    for i in range(N_c): #loop over rows
        idx_ok = np.argwhere( (rij[i] < cutoff) ) [:,0]
        coord_array=np.append(coord_array,len(idx_ok))
        
        list_ok=[]
        for id in idx_ok:
            list_ok.append(idx_n[id])
        
            #print(list_ok)
        idx_prev_n.append(list_ok)

    return coord_array, idx_prev_n

##############################

def run_analysis(folder,file_traj,elem_c,elem_n,cutoff,cutoff_build,outfile):

    time0=t.perf_counter()
    traj=load_traj(folder+"/"+file_traj)
    time1=t.perf_counter()
    
    print(str(time1-time0)+" s to read the trajectory")
    
    step=0
    
    for atoms in traj[:]: #do the full analysis (without plots)
       # print(atoms)
        mycell=atoms.cell
        box=mycell.lengths()
        
        
        if(step==0):
            Ntot,N_c,N_n=info_from_conf(atoms,elem_c,elem_n) #extract info from config
            rij=np.zeros((N_c,N_n)) #centers-neighbors distances
            coord_array=np.empty(N_c)
            atoms_c,atoms_n,idx_c,idx_n=split_cen_neigh(atoms,elem_c,elem_n) # split into centers and neighbors
            #print(idx_c)
            atoms.set_pbc(True)
            atoms.set_cell(box)
            
            print(N_c,N_n)
        
        coord_prev=coord_array #save previous step
        
        if(step!=0):
            rebuild=check_rebuild(atoms,idx_c,idx_prev_n,cutoff_build)
        else:
            rebuild=True
            
        if (rebuild==True):
            print("rebuilding at step..."+str(step))
            coord_array,idx_prev_n=compute_coord(N_c,N_n,atoms_c,atoms_n,idx_c,idx_n,atoms,box,cutoff,rij) #compute NH coordination (NH-c)
        atoms_c.set_array('coordNH',coord_array)
                
        write(outfile,atoms_c,append=True) #re-write trajectory with NH-c
            
        #detect transfers
        if (np.array_equal(coord_array,coord_prev)==False and step!=0):
            diff_array = np.where((coord_array-coord_prev) != 0)
            i=0
            for elem in diff_array:
                #print(elem)
                print("Proton transfer at step "+str(step))  #", one H moved from N #{} to #{}".format(,))
                for el in diff_array:
	                print(idx_c[int(el)])
                i=i+1
        
        step+=1

    return
################################################################################################################

#read traj
folder="./"
outfile=sys.argv[2]
cutoff=1.5 #A
cutoff_build=1.3 #if one N-H bond gets longer than this, rebuild lists

os.system("test -f "+str(outfile)+" && rm "+str(outfile))

run_analysis(folder,input_file,"N","H",cutoff,cutoff_build,outfile) #adjust without chem symb
