# Written by Francesco Mambretti
# 13/10/2023 version


### import
import matplotlib.pyplot as plt
import matplotlib.cm as cm2
from matplotlib.colors import LogNorm
import numpy as np
import math,sys,os
import glob
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.interpolate import BSpline, make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.interpolate import BSpline, make_interp_spline
from scipy.optimize import curve_fit
import pandas as pd

### define functions

##################################################################
def readXYZ_full(file_open):
    # Read essential information: z and displacement
    Dis_list = []
    Z_list  = []
    atoms = []
    coord_list = []
    #Dis_list_Z = []

    with open(file_open, 'r') as f:
        for line in f:
            #print(line)
            try:
                natm = int(line)  # Read number of atoms
                next(f)     # Skip over comments
                z = []
                disp = []
                #disp_Z = []
                cn = []
                for i in range(natm):
                    line = next(f).split()
                    if (len(atoms)<natm):
                        atoms.append(line[1]) #atom_type
                    disp.append(float(line[6]))
                    #disp_Z.append(float(line[7]))
                    z.append(float(line[4]))
                    cn.append(float(line[5]))
                Dis_list.append(disp)
                Z_list.append(z)
                coord_list.append(cn)
                #Dis_list_Z.append(disp_Z)
            except (TypeError, IOError, IndexError, StopIteration):
                raise ValueError('Incorrect XYZ file format')
    print('Close file:',file_open)
    
    return Dis_list, Z_list, atoms, coord_list #Dis_list, Dis_list_Z, Z_list, atoms, coord_list


##################################################################
def build_np_arrays(Dis_list,Z_list,atoms):
    atoms_arr = np.asarray(atoms)
    Dis_arr  = np.asarray(Dis_list)
    Z_arr = np.asarray(Z_list)

    # Check array dimension
    print('Atom:', np.shape(atoms_arr))
    print('Z:', np.shape(Z_arr))
    print('Displacements:', np.shape(Dis_arr))
    
    return Dis_arr, Z_arr, atoms_arr


##################################################################
def displ_per_layer(num_lay,atom_type,z_refs,Dis_arr,Z_arr,atoms):
    
    num_frames,num_atoms=np.shape(Z_arr)

    dis_lay_all=[]
    dis_lay_0=np.empty(0)
    
    Dis_arr=Dis_arr.ravel()
    Z_arr=Z_arr.ravel()
    
    z0=z_refs[0]
    print(num_frames,np.shape(Dis_arr),np.shape(Z_arr))

    for at in range (0,num_atoms):
        if(atoms[at]==atom_type):
            for f in range (0,num_frames):
                index=f*num_atoms+at
                if(Z_arr[index] >=z0):
                    dis_lay_0=np.append(dis_lay_0,Dis_arr[index])

    print ("In layer 0, we have {} displacements".format(len(dis_lay_0)))
           
    #dis_lay_all=np.append(dis_lay_all,dis_lay_0)
    if(len(dis_lay_0)==0):
        dis_lay_0=[0]
        
    dis_lay_all.append(dis_lay_0)
    
    for i in range(1,num_lay):
        z1=z_refs[i]
        dis_lay_i=np.zeros(0)
        for at in range (0,num_atoms):
            if (atoms[at]==atom_type):
                for f in range (0,num_frames):
                    index=f*num_atoms+at
                    if (Z_arr[index] <z0 and  Z_arr[index] >=z1):
                        dis_lay_i=np.append(dis_lay_i, Dis_arr[index])
        z0=z1
        
        print ("In layer "+str(i)+", we have {} displacements".format(len(dis_lay_i)))
        dis_lay_all.append(dis_lay_i)
               
    return dis_lay_all
    
##################################################################
def displ_single_layer(which_lay,atom_type,z_refs,Dis_arr,Z_arr,atoms):
    
    num_frames,num_atoms=np.shape(Z_arr)

    dis_lay=np.empty(0)
    
    Dis_arr=Dis_arr.ravel()
    Z_arr=Z_arr.ravel()
    
    print(num_frames,np.shape(Dis_arr),np.shape(Z_arr))
    
    if (which_lay==0):
        z0=z_refs[0]

        for at in range (0,num_atoms):
            if(atoms[at]==atom_type):
                for f in range (0,num_frames):
                    index=f*num_atoms+at
                    if(Z_arr[index] >=z0):
                        dis_lay=np.append(dis_lay,Dis_arr[index])

        print ("In layer 0, we have {} displacements".format(len(dis_lay)))
           
        if(len(dis_lay)==0):
            dis_lay=[0]
    
    else:
        z0=z_refs[which_lay-1]
        z1=z_refs[which_lay]
        
        for at in range (0,num_atoms):
            if (atoms[at]==atom_type):
                for f in range (0,num_frames):
                    index=f*num_atoms+at
                    if (Z_arr[index] <z0 and  Z_arr[index] >=z1):
                        dis_lay=np.append(dis_lay, Dis_arr[index])
            
        print ("In layer "+str(which_lay)+", we have {} displacements".format(len(dis_lay)))
               
    return dis_lay
    
##################################################################
def displ_per_layer_and_coord(num_lay,atom_type,z_refs,Dis_list,Z_list,atoms,coord,coordKey,num_atoms):
    
    dis_lay_all=[]
    dis_lay_0=[]
    
    z0=z_refs[0]
    print(z0,np.shape(Dis_list),np.shape(Z_list),np.shape(coord))
    #dis_lay_0=Dis_list[np.logical_and(np.logical_and((Z_list>=z0),(atoms==atom_type)),(coord==coordKey))]
    n_frames=len(Z_list) #first dimension
    
    for f in range (0,n_frames):
        for at in range (0,num_atoms):
            if (atoms[at]==atom_type and Z_list[f][at] >=z0 and coord[f][at]==coordKey):
                dis_lay_0.append(Dis_list[f][at])
            #Dis_list[f][np.logical_and(np.logical_and((Z_list[f]>=z0),(coord[f]==coordKey)),(atoms ==atom_type))])
    
    print ("In layer 0, we have {} displacements".format(len(dis_lay_0)))
           
    dis_lay_all.append(dis_lay_0)
    
    for i in range(1,num_lay):
        z1=z_refs[i]
        dis_lay_i=np.zeros(0)
        for f in range (0,n_frames):
            for at in range (0,num_atoms):
                if (atoms[at]==atom_type and Z_list[f][at] <z0 and  Z_list[f][at] >=z1 and coord[f][at]==coordKey):
                    dis_lay_i=np.append(dis_lay_i, Dis_list[f][at])
        z0=z1
        #Dis_list[f][np.logical_and(np.logical_and((Z_list[f]>=z0),(coord[f]==coordKey)),(atoms ==atom_type))])
    
        print ("In layer "+str(i)+", we have {} displacements".format(len(dis_lay_i)))
        dis_lay_all.append(dis_lay_i)
               
    return dis_lay_all
    
##################################################################

def build_z_profile_coord(num_lay,atom_type,Z_list,atoms,coord,coordKey,num_atoms,mycolor): #old
    
    z_values=[]
    n_frames=len(Z_list) #first dimension
    
    #for each frame, select only the relevant z values
    for f in range (0,n_frames):
        for at in range (0,num_atoms):
            if (atoms[at]==atom_type and coord[f][at]==coordKey):
                z_values.append(Z_list[f][at])
     
    #compute histogram of the Z_values
    Nbins=300
    prob,edges=np.histogram(z_values,bins=Nbins,range=(5,25),density=True) #range in Angstrom

    bin_centers=np.zeros(Nbins)
    for j in range (0,Nbins):
        bin_centers[j]=(edges[j+1]+edges[j])*0.5 #compute the arithmetic mean
    
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False, figsize=(9, 6))
    
    ax.bar(bin_centers,prob,color=mycolor,edgecolor='black',width=0.1)
    ax.set_xlim(5,25)
    
    plt.show()
               
    return  bin_centers,prob

##################################################################

def build_z_profile(num_lay,atom_type,Z_list,atoms,num_atoms,mycolor): #old
    
    z_values=[]
    n_frames=len(Z_list) #first dimension
    
    #for each frame, select only the relevant z values
    for f in range (0,n_frames):
        for at in range (0,num_atoms):
            if (atoms[at]==atom_type):
                z_values.append(Z_list[f][at])
     
    #compute histogram of the Z_values
    Nbins=300
    prob,edges=np.histogram(z_values,bins=Nbins,range=(5,25),density=True) #range in Angstrom

    bin_centers=np.zeros(Nbins)
    for j in range (0,Nbins):
        bin_centers[j]=(edges[j+1]+edges[j])*0.5 #compute the arithmetic mean
               
    return bin_centers,prob

##################################################################

def clean_lists(Dis_list,Z_list,atoms): #old
    del Z_list
    del atoms
    del Dis_list

##################################################################

def scatterplot_all(num_lay,dis_lay_all): #old
    fig, axs = plt.subplots(nrows=1, ncols=num_lay, sharex=False, sharey=False, figsize=(20, 5))
    
    for i in range (0,num_lay):
        myax=axs[i]

        myX=np.arange(len(dis_lay_all[i]))

        myax.plot(myX,dis_lay_all[i],'b-o',alpha=0.5)

        myax.set_title('layer {}'.format(i),fontsize = 14)

        myax.set_ylabel('Displacements',fontsize=14)

    plt.show()
    

##################################################################

def split_trajs(nruns,num_atoms,frames_per_file,total_lines_per_file,folder): #split to analyze faster

	for i in range (nruns):
		lines_per_file=frames_per_file*(num_atoms+2) #lines in *part* files
		iters=int(total_lines_per_file[i]/lines_per_file)
		print(i,iters)
		for a in range(iters):     
			start=a*lines_per_file+1
			end=(a+1)*lines_per_file
			#os.system("sed -n '"+str(start)+","+str(end)+"p;' "+folder+"/dump."+str(i)+".displ.xyz  > "+folder+"/dump.part."+str(a)+"_"+str(i)+".xyz")
			os.system("sed -n '"+str(start)+","+str(end)+"p;' "+folder+"/dump.displ."+str(i)+".xyz  > "+folder+"/dump.part."+str(a)+"_"+str(i)+".xyz")
	return

##################################################################

def analyze_traj(num_lay,nruns,iters,path,num_atoms):
    

    for r in range (0,nruns):
    	#reset counters
        count_z_layers=[0,0,0]
        f_z_layers = open(path+"/count_z_layers."+str(r)+".txt", "w") 
    
        for i in range (0,iters): #iters
            print(r,i)
            myfile=path+'/dump.part.'+str(i)+'_'+str(r)+'.xyz'
            print(myfile)
            Dis_list, Z_list, atoms, coord=readXYZ_full(myfile)
            Dis_arr, Z_arr, atoms_arr=build_np_arrays(Dis_list,Z_list,atoms)
            
            #save the list of all z coordinates, divided by species (and also NH/NH2)
            f_Li = open(path+"/all_z_Li.txt", "a")
            f_N = open(path+"/all_z_N.txt", "a")            
            f_H = open(path+"/all_z_H.txt", "a")
            f_NH = open(path+"/all_z_NH.txt", "a")
            f_NH2 = open(path+"/all_z_NH2.txt", "a")            

            for z,c in zip(Z_arr,coord):     
                count_z_layers=[0,0,0] #at each step, reset     	
                for j in range (0,num_atoms):
                    if atoms_arr[j]=="Li":
                        f_Li.write("%s\n" % z[j])
                    elif atoms_arr[j]=="H":
            	        f_H.write("%s\n" % z[j])
                    elif atoms_arr[j]=="N":
                        f_N.write("%s\n" % z[j])
                        if c[j]==1: #NH
                            f_NH.write("%s\n" % z[j])
               	        elif c[j]==2: #NH2
                            f_NH2.write("%s\n" % z[j])
                            
		 				#check effective occupancy of layers at each time, limited to Nitrogens
                        if (z[j]>z_refs[0]):
                            count_z_layers[0]+=1
                        elif (z[j] <= z_refs[0] and z[j]>z_refs[1]):
                            count_z_layers[1]+=1
                        elif (z[j] <= z_refs[1] and z[j]>z_refs[2]):
                            count_z_layers[2]+=1
					
                f_z_layers.write("%s %s %s \n" % (count_z_layers[0],count_z_layers[1],count_z_layers[2])) #save, at each time, the count of Nitrogen atoms in each layer 
            
            f_Li.close()
            f_N.close()
            f_H.close()
            f_NH.close()
            f_NH2.close()
              	            
          	#save the list of all displacements
            for l in range (num_lay):
                list_displ=displ_single_layer(l,atom_type,z_refs,Dis_arr,Z_arr,atoms_arr)
                
                with open (path+"/all_displ."+str(l)+".txt", "a") as outfile:
                    for item in list_displ:
                        outfile.write("%s\n" % item)
                        
    f_z_layers.close()
             
    return
    
####################################################################################################################################

# Separate NH and NH2

## pre - NH$_3$ addition
atom_type='N' #nitrogen
z_refs=[21,18,15,12]
nruns=4
iters=10
num_lay=3
root_path="/home/fmambretti@iit.local/Documents/Li_NH_NH2/displacements/"
conc=[0,10,20]
split=False
anal=True
groups=["Li","N","H","NH","NH2"]
Nbins=400
num_atoms=384
frames_per_file=11500

total_lines_per_file=[[46319614,46319614,46319614,46319614],[46319614,46319614,46319614,46319614]]

for i,c in enumerate(conc): #pre-NH3 addition
    path=root_path+str(c)+"_NH2_pre/"
    os.system("rm "+path+"all*") #clean
	
    if split==True:
        split_trajs(nruns, num_atoms, frames_per_file, total_lines_per_file[i], path)
    if anal==True:
        analyze_traj(num_lay,nruns,iters,path,num_atoms)

    ## build histograms and save them in text files
    for g in groups:
        try:
            data_z=pd.read_csv(path+"/all_z_"+str(g)+".txt",).to_numpy()
            print(data_z[0])
        except:
            data_z=np.zeros(100)
        prob,edges=np.histogram(data_z,bins=Nbins,density=True)

        bin_centers=np.zeros(Nbins)
        for j in range (0,Nbins):
            bin_centers[j]=(edges[j+1]+edges[j])*0.5 #compute the arithmetic mean        
            np.savetxt(path+"/histo_z_"+str(g)+".txt",np.column_stack((bin_centers,prob)))
   
    
##################################################################

## ## post - NH3 addition

total_lines_per_file=[[46319614,46319614,46319614,46319614],[46319614,46319614,46319614,46319614]] 

Nbins=900
num_atoms=392
conc=[0,10,20,]

for i,c in enumerate(conc): #post-NH3 addition
    path=root_path+str(c)+"_NH2_post/"
    os.system("rm "+path+"all*") #clean
	
    if split==True:
        split_trajs(nruns,num_atoms, frames_per_file, total_lines_per_file[i], path)
    if anal==True:
        analyze_traj(num_lay,nruns,iters,path,num_atoms)



## build histograms and save them in text files
    for g in groups:
        try:
            data_z=pd.read_csv(path+"/all_z_"+str(g)+".txt",).to_numpy()
        except:
            data_z=np.zeros(100)
        prob,edges=np.histogram(data_z,bins=Nbins,density=True)

        bin_centers=np.zeros(Nbins)
        for j in range (0,Nbins):
            bin_centers[j]=(edges[j+1]+edges[j])*0.5 #compute the arithmetic mean        
            np.savetxt(path+"/histo_z_"+str(g)+".txt",np.column_stack((bin_centers,prob)))

