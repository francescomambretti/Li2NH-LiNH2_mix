# Python script to add hydrogens to transform NH into NH2
# written by Francesco Mambretti, 15/12/2022
# 04/01/2022 version

import sys
import os
import numpy as np
from numpy.random import rand,seed
import math
from numpy.linalg import norm

if (len(sys.argv)!=5):
    print("Error! 4 arguments needed: input file, output file, random seed, N to substitute")

input_file=sys.argv[1]
output_file=sys.argv[2]

#set params
myseed=sys.argv[3] #set seed
seed(int(myseed))

angle=2./3.*np.pi #radians, planar molecule angle
N=int(sys.argv[4]) #hydrogens to add --> MUST be even! 1 NH has 2 "-" charges, while 1 NH_2 has only one "-" charge
Hydro_t=1
Nitro_t=2
Lithium_t=3

lammps_offset=10

#global variables
x=np.zeros(0)
y=np.zeros(0)
z=np.zeros(0)
id=np.zeros(0)
type=np.zeros(0)

##################################################################################################################################
#methods definition

def rotation_matrix_from_vectors(vec1,vec2):

    a, b = (vec1 / norm(vec1)).reshape(3), (vec2 / norm(vec2)).reshape(3)
    v = np.cross(a, b)
    if any(v): #if not all zeros then
        c = np.dot(a, b)
        s = norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    else:
        return np.eye(3) #cross of all zeros only occurs on identical directions


####################################
def read_input(input_file): #LAMMPS format
    id,type,x,y,z=np.loadtxt(input_file,skiprows=9,unpack=True) #coordinates are already in PBC
    hydrogens=id[type==Hydro_t] #save indexes of hydrogens
    nitrogens=id[type==Nitro_t] #same for nitrogens
    lithii=id[type==Lithium_t] #lithii
    
    return hydrogens,nitrogens,lithii,id,type,x,y,z

####################################
def gen_new_coords(index,neigh_index,min_dist):
    #the new H atom must have same x and z as neigh_index, i.e. the Hydrogen already present
    
    i1=int(np.where(id==index)[0])
    i2=int(np.where(id==neigh_index)[0])
    
    a1x=pbc(x[i2]-x[i1],0) #compute N-H distance
    a1y=pbc(y[i2]-y[i1],1)
    a1z=pbc(z[i2]-z[i1],2)
    
    a1=(a1x,a1y,a1z)
    min_dist=np.sqrt(a1x*a1x+a1y*a1y+a1z*a1z) #compute its norm
    a1p=(min_dist,0,0)
    
    #move all into a new reference frame, where the H already present lies at a distance min_dist along x axis
    transform_matrix=rotation_matrix_from_vectors(a1, a1p)
    
    theta=2./3.*np.pi
    a2px=min_dist*np.cos(theta)
    a2py=min_dist*np.sin(theta)
    a2pz=0
    
    a2p=(a2px,a2py,a2pz)
    
    #print(np.degrees(np.arccos(np.dot(a1p,a2p)/(norm(a1p)*norm(a2p)))))
    
    a2=np.matmul(transform_matrix.T,a2p)
    
    #print(np.degrees(np.arccos(np.dot(a1,a2)/(norm(a1)*norm(a2)))))
    
    new_x=a2[0]+x[i1]
    new_y=a2[1]+y[i1]
    new_z=a2[2]+z[i1]
    
    
    #print( new_x,new_y,new_z)
    
    return new_x,new_y,new_z

####################################
def compute_mat_dist(species1,species2,N1,N2,x,y,z):

    mat_dist=np.zeros((N1,N2))

    for a,i in zip(species1,range(0,N1)):
        k = int(np.where(id==a)[0])
        for b,j in zip(species2,range(0,N2)):
            l=int(np.where(id==b)[0])
            mat_dist[i][j]=np.sqrt(pbc(x[k]-x[l],0)*pbc(x[k]-x[l],0)+pbc(y[k]-y[l],1)*pbc(y[k]-y[l],1)+pbc(z[k]-z[l],2)*pbc(z[k]-z[l],2))
            
            #check possible errors
            if(mat_dist[i][j]>box[0]*np.sqrt(3)/2.):
                print(k,l,x[k],y[k],z[k],x[l],y[l],z[l],pbc(x[k]-x[l],0),pbc(y[k]-y[l],1),pbc(z[k]-z[l],2),mat_dist[i][j])
                print("Error!")
                return
            
    return mat_dist
    
####################################
def compute_vec_dist(species1,N1,x,y,z,x_new,y_new,z_new):

    vec_dist=np.zeros(N1)

    for a,i in zip(species1,range(0,N1)):
        k = int(np.where(id==a)[0])
        vec_dist[i]=np.sqrt(pbc(x[k]-x_new,0)*pbc(x[k]-x_new,0)+pbc(y[k]-y_new,1)*pbc(y[k]-y_new,1)+pbc(z[k]-z_new,2)*pbc(z[k]-z_new,2))
     
        #check possible errors
        if(vec_dist[i]>box[0]*np.sqrt(3)/2.):
            print(k,x[k],y[k],z[k],x_new,y_new,z_new,pbc(x[k]-x_new,0),pbc(y[k]-y_new,1),pbc(z[k]-z_new,2),vec_dist[i])
            print("Error!")
            return
            
    return vec_dist
    
        
####################################

def pbc(length,comp):
    return length - box[comp] * (np.round(length/box[comp]))
    

def delete_lithium_atom(lithii,N_Lithium,id,type,x,y,z,x_new,y_new,z_new):
    #delete the Li atom which is the closest to the added Hydrogen
    #compute the distance of all the Li atoms from the added H
    dist_Li_newH = compute_vec_dist(lithii,N_Lithium,x,y,z,x_new,y_new,z_new)
    
    #find closest lithium to the added H
    min_dist=np.min(dist_Li_newH)
    inner_index=int(np.where(dist_Li_newH==min_dist)[0]) #internal index among the group of Li atoms
    index_to_del=int(np.where(id==lithii[inner_index])[0])
    
    print("Deleting Li atom number {}, found at position {}".format(int(id[index_to_del]),int(index_to_del+lammps_offset)))
    
    #delete
    id=np.delete(id,index_to_del)
    type=np.delete(type,index_to_del)
    x=np.delete(x,index_to_del)
    y=np.delete(y,index_to_del)
    z=np.delete(z,index_to_del)
    
    return lithii[inner_index],id,type,x,y,z


##################################################################################################################################

Ntotal=np.loadtxt(input_file,skiprows=1,max_rows=1,unpack=True,usecols=(0,)) #read total number of atoms

#set box size
boxx_lo, boxx_hi = np.loadtxt (input_file,skiprows=3,max_rows=1,unpack=True,usecols=(0,1))
boxy_lo, boxy_hi = np.loadtxt (input_file,skiprows=4,max_rows=1,unpack=True,usecols=(0,1))
boxz_lo, boxz_hi = np.loadtxt (input_file,skiprows=5,max_rows=1,unpack=True,usecols=(0,1))

box=np.zeros(3)
box[0]=boxx_hi-boxx_lo
box[1]=boxy_hi-boxy_lo
box[2]=boxz_hi-boxz_lo

#read input
hydrogens,nitrogens,lithii,id,type,x,y,z=read_input(input_file)

hydrogens=np.asarray(hydrogens,dtype=int)
nitrogens=np.asarray(nitrogens,dtype=int)
lithii=np.asarray(lithii,dtype=int)

N_Hydro=len(hydrogens)
N_Nitro=len(nitrogens)
N_Lithium=len(lithii)

#compute N-H distances matrix
mat_dist=compute_mat_dist(nitrogens,hydrogens,N_Nitro,N_Hydro,x,y,z)

#add hydrogens in random positions

for i in range (0,N):

    j=int(rand()*N_Nitro) #choose random nitrogen atom
    index=int(nitrogens[j]) #true atom ID
    #print(index,int(type[id==index]))
    #generate new coordinates for the new H, bonded to the chosen Nitrogen atom, whose index is id[nitrogens[j]]
    min_dist=np.min(mat_dist[j]) #choose the H with the minimum distance, in the j-th row
    k=int(np.where(mat_dist[j]==min_dist)[0]) #select the closest hydrogen to the chosen nitrogen, k-th column of j-th row
    neigh_index=int(hydrogens[k])
    #print(index,int(type[id==index]),neigh_index,int(type[id==neigh_index]))
    x_new,y_new,z_new=gen_new_coords(index,neigh_index,min_dist)
    #print(id[index],type[int(id[index])],neigh_index,type[int(neigh_index)])
    index_to_add,id,type,x,y,z=delete_lithium_atom(lithii,N_Lithium,id,type,x,y,z,x_new,y_new,z_new)

    #update
    N_Lithium-=1
    N_Hydro+=1
    x=np.append(x,x_new)
    y=np.append(y,y_new)
    z=np.append(z,z_new)
    id=np.append(id,index_to_add) #the new H atom takes the id of the deleted Li
    type=np.append(type,Hydro_t)

#print new file
#read first 9 lines
with open(input_file, 'r') as fp:
    line0 = fp.readlines()[0:1]
with open(input_file, 'r') as fp:
    lines3_9 = fp.readlines()[3:9]
    
with open(output_file, 'w') as f:
    f.write(line0[0])
    f.write(str(int(Ntotal))+" atoms \n")
    f.write(str(int(np.max(type)))+" atom types \n")
    for line in lines3_9:
        f.write(line)
    for a,b,c,d,e in zip(id,type,x,y,z):
        f.write(str(int(a))+" "+str(int(b))+" "+str(c)+" "+str(d)+" "+str(e)+"\n")

    f.close()

