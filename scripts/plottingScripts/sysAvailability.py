import numpy as np
import matplotlib.pyplot as plt
import json

plt.style.use('seaborn-ticks')

def funcFormatter(val, idx):
    return "{:4d}%".format(int(val*100))

# for the simulated system availability
ndc=0.15 

# the average benefit of adding an INode is tot = (1-tot) * ndc +tot
def tot(n,ndc):
    assert ValueError(n >0 and ndc <= 1)
    onTime=0
    coverage=[]
    for i in range(n):
        onTime += (1 - onTime) * ndc
        coverage.append(onTime)
    return np.array(coverage)

# Load Data 
# path = '../processed_data/paper_availability680.json'
path = '../processed_data/new/availability470.json'
data=[]
with open(path) as f:
    for l in f:
        data.append(json.loads(l))

n=len(data[0][1])
# Plotting
## Figure, Axes setup
fig = plt.figure(figsize=(8,4))
ax = plt.axes()
ax.grid(linestyle=":")

## Plotting parameters 
colors = ["#2b8cbe","#2b8cbe","#2b8cbe","#2b8cbe", "#d73027" ]
plotPatterns = ['-*', '->', '-d','-o', '-+']
fontSize = 18 
#colors=['r','b','k']
dataIndices = np.arange(len(data[0][1]))+1 

# for idx, d in enumerate(data):
#     print(np.mean(d[1]))
# exit()

## Data plotting
for idx, d in enumerate(data):
    #print(d[0])
    # print("Data length", len(d[1]) )
    print(np.array(d[1])*10)
    ax.plot(dataIndices, np.array(d[1])*10,plotPatterns[idx], label=d[0], markersize = 8, lw=2, color=colors[idx] ) #, color=colors[idx]) 

# Plotting the simulated system availability 
ax.plot(range(1,n+1), tot(n,ndc)* 10, '--', label="{:0.0f}%".format(100*ndc), lw=3, color=colors[-1])

## axes formatting 
ylabels = ["{:4d}%".format(x*10) for x in range(1,11,2)]
ax.set_yticks(range(1,11,2))
ax.set_yticklabels(ylabels, fontsize=fontSize)
ax.set_xticklabels(dataIndices, fontsize=fontSize)
ax.set_xticks(dataIndices)
ax.set_ylabel("Availability", fontsize=fontSize)
ax.set_xlabel("Number of nodes", fontsize=fontSize)
## Plotting output
# ax.legend(frameon=False, fontsize=fontSize-2, loc="upper left")
ax.legend(frameon=False, fontsize=fontSize-2, loc="lower right")
plt.tight_layout()
# plt.savefig('../../paper/figures/new_sysAvailability.eps')
plt.savefig('../../paper/figures/new_sysAvailability_artificial-light.eps')

plt.show()
