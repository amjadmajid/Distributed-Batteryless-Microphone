import matplotlib.pyplot as plt
import numpy as np
import sys, os, json


files = [
"524-541lux.json",
"812-836lux.json",
"1400-1413lux.json",
"1705-1737lux.json"
]

#### Separate plots
# for file in files:
#     with open(file, "r") as read_file:
#         data = json.load(read_file)

#     f = plt.figure(figsize=(8,4))
#     plt.ylim(-0.5, 8.5)
#     plt.xlabel("Events")
#     plt.ylabel("Detection count")
#     plt.boxplot(data)
#     f.savefig(file.split(".")[0]+".pdf", bbox_inches='tight')
# plt.show()



color_list = ['r', 'k', 'b', 'g']
f = plt.figure(figsize=(8,4))
for i in range(len(files)):
    file = files[i]
    with open(file, "r") as read_file:
        data = json.load(read_file)

    medianprops = {'color':color_list[i], 'linewidth': 2}
    boxprops = {'color': color_list[i], 'linestyle': '-'}
    whiskerprops = {'color': color_list[i], 'linestyle': '-'}
    capprops = {'color': color_list[i], 'linestyle': '-'}
    flierprops = {'color': color_list[i], 'marker': 'x'}
    
    plt.xlabel("Events")
    plt.ylabel("Detection count")
    plt.boxplot(data, positions=np.arange(4)+5*i, widths=0.5, medianprops=medianprops, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, flierprops=flierprops, labels=[1,2,3,4])
    plt.ylim(-0.5, 8.5)
    plt.xlim(-0.2, 20)

f.savefig("combined.pdf", bbox_inches='tight')
plt.show()