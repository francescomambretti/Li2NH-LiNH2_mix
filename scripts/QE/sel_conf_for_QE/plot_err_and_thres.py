# written by Francesco Mambretti
# 08/05/2023
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

thresh=np.quantile(devs,levels)
counts=thresh*len(devs)
counts=list(map(int,counts))

print("The sigma values are:  {:.2f}, {:.2f}, {:.2f} and {:.2f}".format(*thresh))
print("There are {}, {}, {} and {} configurations in each group, respectively".format(*counts))

for t in thresh:
    plt.axvline(x = t, color = 'b', ymin = 0, ymax = 0.95)

plt.hist(devs,bins=100,color='gold')
plt.xlabel("Deviations [eV/$\AA$]",fontsize=16)
plt.show()
                                         
