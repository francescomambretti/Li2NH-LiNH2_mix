# written by Francesco Mambretti
# 10/05/2023
# plot the distribution of the errors associated to the LAMMPS configurations, together with vertical lines in correspondence of the selected thresholds
# cmd line arguments: path to model_devi.out & levels for slicing the distribution of deviations

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

if (len(sys.argv)!=6):
    print("Required: path to model_devi.out & 4 levels (to be used as quantiles of the deviations distribution)")
    sys.exit(-1)

path=sys.argv[1]
levels=sys.argv[2:6]
levels=list(map(float, levels))
print(levels)

devs=np.loadtxt(path+"/model_devi.out",usecols=(4),unpack=True)
print("There are, in total, {} frames".format(int(len(devs))))

thresh=np.quantile(devs,levels)
counts=[0,0,0,0,0]

counts[0]= sum(d<thresh[0] for d in devs)
for i in range(1,4):
    counts[i]=sum((d<thresh[i] and d>=thresh[i-1]) for d in devs)
counts[4]= sum(d>=thresh[3] for d in devs)

print("The sigma values are:  {:.4f}, {:.4f}, {:.4f} and {:.4f}".format(*thresh))
print("There are {}, {}, {}, {} and {} configurations in each group, respectively".format(*counts))

for t in thresh:
    plt.axvline(x = t, color = 'b', ymin = 0, ymax = 0.95)

plt.hist(devs,bins=100,color='gold')
plt.xlabel("Deviations [eV/$\AA$]",fontsize=13)
plt.show()
                                         
