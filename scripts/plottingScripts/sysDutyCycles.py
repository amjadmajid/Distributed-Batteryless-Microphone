import numpy as np
import matplotlib.pyplot as plt
import json

plt.style.use('seaborn-whitegrid')

# Load Data 
path = '../processed_data/sysDutyCycles680.json'
data=[]
with open(path) as f:
    for l in f:
        data.append(json.loads(l))

# Plotting
## Figure, Axes setup
fig = plt.figure(figsize=(8,4))
ax = plt.axes()
ax.grid(linestyle=":")

## Plotting parameters 
fontSize = 16 

maxVal=-1000
for i in range(len(data)):
    if maxVal < max( max(data[i][1])):
            maxVal =max( max(data[i][1]))

dataIndices = np.arange(int(maxVal))+2
print(maxVal)
print(dataIndices)
colors=['r','b','k']
## Data plotting
box=[]
for idx, d in enumerate(data):
    #print(d[0])
    #print(d[1]) 
    box.append(ax.boxplot(np.array(d[1]), showfliers=False))
    for _, line_list in box[idx].items():
        for line in line_list:
            line.set_color(colors[idx])
            line.set_linewidth(1.25)

## axes formatting 
ylabels = ["{:4d}%".format(x*10) for x in dataIndices-1]
ax.set_yticks(dataIndices-1)
ax.set_yticklabels(ylabels, fontsize=fontSize)
ax.set_xticklabels(range(1,9), fontsize=fontSize)
ax.set_xticks(range(1,9))

ax.legend([box[0]["boxes"],box[1]["boxes"], box[1]["boxes"]], ['A', 'B','C'] )
## Plotting output
#ax.legend(frameon=False, fontsize=fontSize)
plt.tight_layout()
plt.savefig('../../paper/figures/sysDutyCycles.eps')
plt.show()

