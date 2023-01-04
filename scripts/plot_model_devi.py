# by Francesco Mambretti
# 04/01/2023 version

import numpy as np
import matplotlib.pyplot as plt
import sys

if (len(sys.argv)<2):
	print("Error! Too few arguments")
	sys.exit(-1)

nfiles=len(sys.argv)-1

for f in range (0,nfiles):
	file=sys.argv[f+1]
	devi=np.loadtxt(file,unpack=True,usecols=(4,))
	plt.plot(devi,marker='o',linestyle='-',label=file)

plt.xlabel("Timestep [ps]")
plt.ylabel("Deviation")
plt.legend()
plt.show()
