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
plotPatterns = ['-*', '-^', '-+','-o', '-d']
fontSize = 16 
#colors=['r','b','k']
dataIndices = np.arange(len(data[0][1])) +1

## Data plotting
for idx, d in enumerate(data):
    #print(d[0])
    # print("Data length", len(d[1]) )
    ax.plot(dataIndices, np.array(d[1])*10,plotPatterns[idx], label=d[0] ) #, color=colors[idx]) 

# Plotting the simulated system availability 
ax.plot(range(1,n+1), tot(n,ndc)* 10, '--', label="{:0.0f}%".format(100*ndc), lw=2)
dataIndicesX = dataIndices
dataIndices = np.append(dataIndices, [9,10,11])
dataIndices = dataIndices[dataIndices %2 != 0]
print(dataIndices)
## axes formatting 
ylabels = ["{:4d}%".format(x*10) for x in dataIndices-1]
ax.set_yticks(dataIndices-1)
ax.set_yticklabels(ylabels, fontsize=fontSize)
ax.set_xticklabels(dataIndicesX, fontsize=fontSize)
ax.set_xticks(dataIndicesX)
ax.set_ylabel("Availability", fontsize=fontSize)
ax.set_xlabel("Number of nodes", fontsize=fontSize)
## Plotting output
ax.legend(frameon=False, fontsize=fontSize, loc='lower right')
plt.tight_layout()
plt.savefig('../../paper/figures/sysAvailability_artificial-light.eps')
plt.show()
