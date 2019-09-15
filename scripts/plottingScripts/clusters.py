import json
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

clusters=[]
with open('../processed_data/clusters.json') as f:
    for cluster in f:
        clusters.append(json.loads(cluster))

print("light intensity & mean & std")

for cluster in clusters:
    #print(cluster)
    m = np.mean(cluster[1])
    sigma =  np.std(cluster[1])
    print('{:15} & {:1.2f} & {:1.2f}\\'.format( cluster[0], m, sigma))
    x = np.linspace(m-3*sigma, m+3*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, m, sigma ))

plt.show()
