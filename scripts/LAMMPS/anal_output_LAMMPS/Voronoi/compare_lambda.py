import numpy as np
import matplotlib.pyplot as plt

colors=['midnightblue','teal','violet','gold']
l_arr=[25,50,75,100]

s=13719
i=0

plt.figure(figsize=(8,8),dpi=300)

for l in l_arr:
    data=np.loadtxt("lambda_"+str(l)+"/NUM_Li.txt",skiprows=s,max_rows=1)
    plt.plot(data,marker='o',linestyle='-',label=str(l),color=colors[i])
    i+=1

plt.xlabel("cell index Voronoi")
plt.ylabel("# Li atoms")
plt.title("Trajectory config. #"+str(s))
plt.tight_layout()
plt.legend(ncol=2,loc='upper center')
plt.show()
