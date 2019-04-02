import numpy as np
import matplotlib.pyplot as plt
import json

# load data
data=[]
with open('../processed_data/availability680.json') as f:
    for l in f:
        data.append(json.loads(l))

for d in data:
    print(d[0])
    print(d[1])
    plt.plot(np.arange(len(d[1]))+1, d[1], label=d[0])

plt.legend()
plt.show()

