# Python script to add hydrogens to transform some NH into NH2
# written by Francesco Mambretti, 15/12/2022
# this code version expects either a LAMMPS dump file or a xyz file (specified by command line)
# the new generated file has the same format of the input one
# This version also deals with surfaces (triclinic cells) --> NH2 are not created in the 2 bottom layers
# 16/03/2023 version - work in progress

import sys
import os
import numpy as np
from numpy.random import rand,seed
from numpy.linalg import norm

if (len(sys.argv)!=8):
    print("Error! 7 arguments needed: input file, input/output format ('dump'/'xyz'), output folder, output file, random seed, N to substitute and triclinic surface(0/1 <--> True/False)")

input_file=sys.argv[1]
format=sys.argv[2]
if (format!='dump' and format!='xyz'):
    print("wrong input file format! set dump or xyz")
    sys.exit(-1)
    
output_folder=sys.argv[3]
output_file=sys.argv[4]

#set params
myseed=sys.argv[5] #set seed
seed(int(myseed))

angle=2./3.*np.pi #radians, planar molecule angle
N=int(sys.argv[6]) #hydrogens to add --> MUST be even! 1 NH has 2 "-" charges, while 1 NH_2 has only one "-" charge
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

surf=int(sys.argv[7]) #whether the box is triclinic or not

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
def read_input(input_file, format): #LAMMPS format
    if format=='dump':
        id,type,x,y,z=np.loadtxt(input_file,skiprows=9,unpack=True) #coordinates are already in PBC
    else: #it is 'xyz'
        type,x,y,z=np.loadtxt(input_file,skiprows=2,unpack=True,dtype=str)
        id=np.arange(0,len(type))
        #convert type into array of integers
        for t in range(0,len(type)):
            if type[t]=="H":
                type[t]=1
            elif type[t]=="N":
                type[t]=2
            elif type[t]=="Li":
                type[t]=3
    
        x=x.astype(float)
        y=y.astype(float)
        z=z.astype(float)
        type=type.astype(float)
        
    hydrogens=id[type==Hydro_t] #save indexes of hydrogens
    nitrogens=id[type==Nitro_t] #same for nitrogens
    lithii=id[type==Lithium_t] #lithii
    
    z_orig=z[type==Nitro_t]
    
    return hydrogens,nitrogens,lithii,id,type,x,y,z,z_orig

####################################
def gen_new_coords(index,neigh_index,min_dist):
    #the new H atom must have same x and z as neigh_index, i.e. the Hydrogen already present
    
    i1=int(np.where(id==index)[0])
    i2=int(np.where(id==neigh_index)[0])
    
    a1x=pbc(x[i2]-x[i1],0) #compute N-H distance
    a1y=pbc(y[i2]-y[i1],1)
    a1z=pbc(z[i2]-z[i1],2)
    
    a1=(a1x,a1y,a1z)
    min_dist=np.sqrt(np.dot(a1,a1)) #compute its norm
    a1p=(min_dist,0,0)
    #print(a1)
    
    #move all into a new reference frame, where the H already present lies at a distance min_dist along x axis
    transform_matrix=rotation_matrix_from_vectors(a1, a1p)
    
    theta=2./3.*np.pi
    a2px=min_dist*np.cos(theta)
    a2py=min_dist*np.sin(theta)
    a2pz=0
    
    a2p=(a2px,a2py,a2pz)
    a2=np.matmul(transform_matrix.T,a2p)
    
    new_x=a2[0]+x[i1]
    new_y=a2[1]+y[i1]
    new_z=a2[2]+z[i1]
    
    return new_x,new_y,new_z

####################################
def compute_mat_dist(species1,species2,N1,N2,x,y,z,surf):

    mat_dist=np.zeros((N1,N2))

    for a,i in zip(species1,range(0,N1)):
        k = int(np.where(id==a)[0])
        for b,j in zip(species2,range(0,N2)):
            l=int(np.where(id==b)[0])
            mat_dist[i][j]=np.sqrt(pbc(x[k]-x[l],0)*pbc(x[k]-x[l],0)+pbc(y[k]-y[l],1)*pbc(y[k]-y[l],1)+pbc(z[k]-z[l],2)*pbc(z[k]-z[l],2))
            #check possible errors
            if (surf==1): #for surfaces, discard
                if(mat_dist[i][j]>box[0]*np.sqrt(3)/2.):
                    print(k,l,x[k],y[k],z[k],x[l],y[l],z[l],pbc(x[k]-x[l],0),pbc(y[k]-y[l],1),pbc(z[k]-z[l],2),mat_dist[i][j])
                    print("Error!")
                    return
                
    return mat_dist
    
####################################
def compute_vec_dist(species1,N1,x,y,z,x_new,y_new,z_new,surf):

    vec_dist=np.zeros(N1)

    for a,i in zip(species1,range(0,N1)):
        k = int(np.where(id==a)[0])
        vec_dist[i]=np.sqrt(pbc(x[k]-x_new,0)*pbc(x[k]-x_new,0)+pbc(y[k]-y_new,1)*pbc(y[k]-y_new,1)+pbc(z[k]-z_new,2)*pbc(z[k]-z_new,2))
     
        #check possible errors
        if (surf==1): #only for bulk
            if(vec_dist[i]>box[0]*np.sqrt(3)/2.):
                print(k,x[k],y[k],z[k],x_new,y_new,z_new,pbc(x[k]-x_new,0),pbc(y[k]-y_new,1),pbc(z[k]-z_new,2),vec_dist[i])
                print("Error!")
                return
            
    return vec_dist
    
        
####################################

def pbc(length,comp):
    return length - box[comp] * (np.round(length/box[comp]))
    
####################################
def delete_lithium_atom(lithii,N_Lithium,id,type,x,y,z,x_new,y_new,z_new,surf):
    #delete the Li atom which is the closest to the added Hydrogen
    #compute the distance of all the Li atoms from the added H
    dist_Li_newH = compute_vec_dist(lithii,N_Lithium,x,y,z,x_new,y_new,z_new,surf)
    
    #find closest lithium to the added H
    min_dist=np.min(dist_Li_newH)
    inner_index=int(np.where(dist_Li_newH==min_dist)[0]) #internal index among the group of Li atoms
    selected_index=lithii[inner_index]
    index_to_del=int(np.where(id==selected_index)[0])
    
    #print("Deleting Li atom number {}, found at position {}".format(int(id[index_to_del]),int(index_to_del+lammps_offset)))
    
    #delete
    id=np.delete(id,index_to_del)
    type=np.delete(type,index_to_del)
    x=np.delete(x,index_to_del)
    y=np.delete(y,index_to_del)
    z=np.delete(z,index_to_del)
    lithii=np.delete(lithii,inner_index)
    
    return selected_index,id,type,x,y,z,lithii
    
    
####################################
def find_box_tr(lx, ly, lz, xy, xz, yz):   #identify triclinic box - may be removed in future versions
    
    #see LAMMPS doc
    a=lx
    b=ly*ly+xy*xy
    c=lz*lz+xz*xz+yz*yz
    
    box_tr=[lx,ly,lz,np.arccos(((xy*xz)+(ly*yz))/(b*c)),np.arccos(xz/c),np.arccos(xy/b)]

    return box_tr
    
####################################
def make_tri_box(boxx_lo_b, boxx_hi_b, boxy_lo_b, boxy_hi_b, boxz_lo_b, boxz_hi_b, xy, xz, yz):  #find triclinic box from orthogonal bounding box
    
    #see LAMMPS doc
    boxx_lo = boxx_lo_b - min(0.0,xy,xz,xy+xz)
    boxx_hi = boxx_hi_b - max(0.0,xy,xz,xy+xz)
    boxy_lo = boxy_lo_b - min(0.0,yz)
    boxy_hi = boxy_hi_b - max(0.0,yz)
    boxz_lo = boxz_lo_b
    boxz_hi = boxz_hi_b
    
    box=[boxx_hi-boxx_lo,boxy_hi-boxy_lo,boxz_hi-boxz_lo] #these are just lengths
    box_list_info=[boxx_hi,boxx_lo,boxy_hi,boxy_lo,boxz_hi,boxz_lo,xy,xz,yz]

    return box, box_list_info

##################################################################################################################################

if format=='dump':
    if (surf==0):
        Ntotal=np.loadtxt(input_file,skiprows=3,max_rows=1,unpack=True,usecols=(0,)) #read total number of atoms
    else:
        Ntotal=np.loadtxt(input_file,skiprows=1,max_rows=1,unpack=True,usecols=(0,)) #read total number of atoms
else: #xyz
    Ntotal=np.loadtxt(input_file,skiprows=0,max_rows=1,unpack=True,usecols=(0,))

#set box size
if (surf==1): #bulk
    if format=='dump':
        boxx_lo, boxx_hi = np.loadtxt (input_file,skiprows=3,max_rows=1,unpack=True,usecols=(0,1))
        boxy_lo, boxy_hi = np.loadtxt (input_file,skiprows=4,max_rows=1,unpack=True,usecols=(0,1))
        boxz_lo, boxz_hi = np.loadtxt (input_file,skiprows=5,max_rows=1,unpack=True,usecols=(0,1))

        box=np.zeros(3)
        box[0]=boxx_hi-boxx_lo
        box[1]=boxy_hi-boxy_lo
        box[2]=boxz_hi-boxz_lo
        
    else:
        pass #complete for xyz

else:
    if format=='dump':
        boxx_lo_b, boxx_hi_b, xy = np.loadtxt (input_file,skiprows=5,max_rows=1,unpack=True,usecols=(0,1,2))
        boxy_lo_b, boxy_hi_b, xz = np.loadtxt (input_file,skiprows=6,max_rows=1,unpack=True,usecols=(0,1,2))
        boxz_lo_b, boxz_hi_b, yz = np.loadtxt (input_file,skiprows=7,max_rows=1,unpack=True,usecols=(0,1,2))
        box,box_list_info=make_tri_box(boxx_lo_b, boxx_hi_b, boxy_lo_b, boxy_hi_b, boxz_lo_b, boxz_hi_b, xy, xz, yz)

    else:
        pass #complete for xyz
        
#read input
hydrogens,nitrogens,lithii,id,type,x,y,z,z_orig=read_input(input_file,format)

hydrogens=np.asarray(hydrogens,dtype=int)
nitrogens=np.asarray(nitrogens,dtype=int)
lithii=np.asarray(lithii,dtype=int)

N_Hydro=len(hydrogens)
N_Nitro=len(nitrogens)
N_Lithium=len(lithii)

#compute N-H distances matrix
mat_dist=compute_mat_dist(nitrogens,hydrogens,N_Nitro,N_Hydro,x,y,z,surf)
#add hydrogens in random positions

#avoid adding two H on the same N
alr_pick=np.empty(0)

for i in range (0,N):

    if i>0:
        while((j in alr_pick) or z_orig[j]<5.2):
            j=int(rand()*N_Nitro) #choose random nitrogen atom
    else:
        j=int(rand()*N_Nitro)
    
    alr_pick=np.append(alr_pick,j)
    #print(j)
    index=int(nitrogens[j]) #true atom ID
    
    #print(index,int(type[id==index]))
    #generate new coordinates for the new H, bonded to the chosen Nitrogen atom, whose index is id[nitrogens[j]]
    min_dist=np.min(mat_dist[j]) #choose the H with the minimum distance, in the j-th row
    #print(min_dist)
    k=int(np.where(mat_dist[j]==min_dist)[0]) #select the closest hydrogen to the chosen nitrogen, k-th column of j-th row
    neigh_index=int(hydrogens[k])
    #print(index,int(type[id==index]),neigh_index,int(type[id==neigh_index]))
    x_new,y_new,z_new=gen_new_coords(index,neigh_index,min_dist)
    #print(id[index],type[int(id[index])],neigh_index,type[int(neigh_index)])
    index_to_add,id,type,x,y,z,lithii=delete_lithium_atom(lithii,N_Lithium,id,type,x,y,z,x_new,y_new,z_new,surf)

    #update
    N_Lithium-=1
    N_Hydro+=1
    x=np.append(x,x_new)
    y=np.append(y,y_new)
    z=np.append(z,z_new)
    id=np.append(id,index_to_add) #the new H atom takes the id of the deleted Li
    type=np.append(type,Hydro_t)
    
    #print (len(lithii))
    
np.savetxt(output_folder+"/list_N_in_NH2_{}.txt".format(N),alr_pick,fmt="%d")

#write new file in the same format
#read first 9 lines

if format=='dump':

    with open(output_folder+"/"+output_file, 'w') as f:
        f.write("LAMMPS data file \n")
        f.write(str(int(Ntotal))+" atoms \n")
        f.write(str(int(np.max(type)))+" atom types \n")
        if (surf==0):
            f.write(str(box_list_info[1])+" "+str(box_list_info[0])+" xlo xhi \n")
            f.write(str(box_list_info[3])+" "+str(box_list_info[2])+" ylo yhi \n")
            f.write(str(box_list_info[5])+" "+str(box_list_info[4])+" zlo zhi \n")
            f.write(str(xy)+" "+str(xz)+" "+str(yz)+" xy xz yz \n")
        else:
            f.write(str(boxx_lo)+" "+str(boxx_hi)+" xlo xhi \n")
            f.write(str(boxy_lo)+" "+str(boxy_hi)+" ylo yhi \n")
            f.write(str(boxz_lo)+" "+str(boxz_hi)+" zlo zhi \n")
        f.write("Atoms \n \n")
        for a,b,c,d,e in zip(id,type,x,y,z):
            f.write(str(int(a))+" "+str(int(b))+" "+str(c)+" "+str(d)+" "+str(e)+"\n")

        f.close()

else: #xyz

    with open(input_file, 'r') as fp:
        lines01 = fp.readlines()[0:2]

    with open(output_folder+"/"+output_file, 'w') as f:
        for line in lines01:
            f.write(line)
        for b,c,d,e in zip(type,x,y,z):
            f.write(str(int(b))+" "+str(c)+" "+str(d)+" "+str(e)+"\n")

        f.close()
