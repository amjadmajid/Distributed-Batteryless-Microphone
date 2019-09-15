import matplotlib.pyplot as plt
import numpy as np
import sys, os, json
plt.style.use('seaborn-ticks')

fontSize=16

labels = ["500lux", "800lux", "1400lux", "1700lux"]
# color_list = ["#66a61e" , '#e7298a', '#7570b3', '#d95f02', '#1b9e77']

# plt.tick_params(axis='x', pad=10, bottom=False)
# intervals = [1,2,4,6]

files = [
"524-541lux.json",
"812-836lux.json",
"1400-1413lux.json",
"1705-1737lux.json"
]

gap = .1
bw = (1-gap)/2

detected = []
captured = []
f = plt.figure(figsize=(8,4))
for i in range(len(files)):
    file = files[i]
    with open("../../data/detection_vs_recognition/"+file, "r") as read_file:
        data = json.load(read_file)
        # labels = data["labels"]
        detected.append(np.mean(data["histDet"][0]))
        captured.append(np.mean(data["histCaptured"][0]))

# print(totalDet)
# print(uniqueDet)
# print()

# totalDet = np.transpose(totalDet)
# uniqueDet = np.transpose(uniqueDet)
# print(totalDet)
# print(uniqueDet)

# for i in range(4):
print(detected)
print(captured)
plt.bar(np.arange(4)+bw, 100*np.array(detected)/np.max(detected), width=bw-0.01, color='#9ecae1', label="detected")
plt.bar(np.arange(4), 100*np.array(captured)/np.max(detected), width=bw-0.01, color='#08519c', label='recognized')

# for i in range(3):
#     plt.axvline(x=0.84+i, color='lightgrey')

# plt.axhline(y=100, color='lightgrey', linestyle=":")

# for group_idx in range(4):

#     for bar_idx in range(4):
#         plt.text( group_idx+bar_idx*bw-0.05 ,-44 , intervals[bar_idx] , color='r' ,fontsize=11, verticalalignment='bottom')


plt.xticks(np.arange(4)+0.225, labels, fontsize=fontSize-2)
plt.yticks(fontsize=fontSize-2)
plt.ylabel("Percent of events (%)", fontsize=fontSize-2)
# plt.xlim([-0.12,3.812])
plt.legend(fontsize=fontSize-2)
plt.tight_layout()
plt.savefig('../../paper/figures/detection_vs_recognition.eps')
plt.show()
