# by Francesco Mambretti
# plot deviation among the 4 models as a function of time & do their histogram
# 11/01/2023 version

import numpy as np
import matplotlib.pyplot as plt
import sys

if (len(sys.argv)<2):
	print("Error! Too few arguments")
	sys.exit(-1)

nfiles=len(sys.argv)-1

nbins=40
histo=np.zeros((nfiles,nbins))
histo_x=np.zeros((nfiles,nbins))


for f in range (0,nfiles):
    file=sys.argv[f+1]
    devi=np.loadtxt(file,unpack=True,usecols=(4,))
    histo[f]=np.histogram(devi,bins=nbins)[0]
    histo_x[f]=np.linspace(devi.min(),devi.max(),num=nbins)
    plt.plot(devi,marker='o',linestyle='-',label=file)

plt.xlabel("Timestep [ps]")
plt.ylabel("Deviation")
plt.legend()
plt.savefig("devi_time.png",dpi=300)

#histogram
plt.clf()

print(histo_x)

for f in range (0,nfiles):
	plt.bar(histo_x[f],histo[f],label=f,width=1e-3,edgecolor='black')

plt.xlabel("Deviation")
plt.legend()
plt.savefig("devi_histo.png",dpi=300)

