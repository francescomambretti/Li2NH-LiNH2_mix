import numpy as np
import matplotlib.pyplot as plt
import os

e=np.loadtxt("energy.raw",unpack=True)

plt.hist(e,bins=100,color='orangered')
plt.savefig("energy_QE.png")
os.system("display energy_QE.png")
