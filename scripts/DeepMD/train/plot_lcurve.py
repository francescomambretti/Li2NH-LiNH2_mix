import numpy as np
import matplotlib.pyplot as plt

main_folder="4GPU-bs4"
num_t=4

for t in range(1,num_t+1):
	steps,data=np.loadtxt(main_folder+"/tr-{}/lcurve.out".format(t),unpack=True,usecols=(0,3))
	plt.plot(steps,data,linestyle='none',marker='o',label="tr-{}".format(t))
plt.xlabel("Training steps",fontsize=15)
plt.ylabel("deviation [eV/atom]",fontsize=15)
plt.xticks((0,5E5,1E6,1.5E6,2E6))
plt.tight_layout()
plt.legend()
plt.yscale('log')
plt.savefig("lcurve.png",dpi=200)
