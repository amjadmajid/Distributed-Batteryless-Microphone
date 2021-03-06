import sys
sys.path.insert(0, '../')
from logicAnalyzerData import *
import matplotlib.pyplot as plt
import numpy as np
import sys, os

plt.style.use('seaborn-ticks')

class Measurement():
    def __init__(self):
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)

    def getDutyCycles(self):
        return [node.avgDutyCycle for node in self.nodes]


class Node():
    def __init__(self, on_times, off_times):
        self.on_times = on_times
        self.off_times = off_times
        self.avgDutyCycle = self.getAverageDutyCycle()

    def getAverageDutyCycle(self):
        on_total = sum(self.on_times)
        off_total = sum(self.off_times)
        duty_cycle = 100* float(on_total)/float(on_total+off_total)
        print("Duty Cycle", duty_cycle)
        return duty_cycle

def boxplot_color_fontsize(box, color, fs):
    for _, line_list in box.items():
        for line in line_list:
            line.set_color(color)
            line.set_linewidth(fs)

def addFile(filename):
    m = Measurement()
    data = LogicAnalyzerData(filename)
    timestamps = data.timestamps
    for nodeNum in range(data.getNumOfNodes()):
        # compute a single node on-time an off-time
        states = data.statesSelector([nodeNum], data.states)
        on_time_flag =  False
        off_time_flag =  False
        on_times=[]
        off_times=[]

        for i in range(1, len(timestamps)):
                state = states[i]
                if (state == 1) and (not on_time_flag):
                    on_time_flag = not on_time_flag
                    on_time_start = timestamps[i]

                if (state == 0) and on_time_flag:
                    on_time_flag = not on_time_flag
                    on_time_end = timestamps[i]
                    on_times.append(on_time_end - on_time_start)

                if (state == 0) and (not off_time_flag):
                    off_time_flag = not off_time_flag
                    off_time_start = timestamps[i]

                if (state == 1) and off_time_flag:
                    off_time_flag = not off_time_flag
                    off_time_end = timestamps[i]
                    off_times.append(off_time_end - off_time_start)

        n = Node(on_times, off_times)
        m.addNode(n)

    # print m.getDutyCycles()
    return m


directory = "../../data/RF/"
# csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
csv_files = ['30cm.csv', '40cm.csv', '50cm.csv', '60cm.csv', '70cm.csv', '80cm.csv'] #, '1705-1737lux.csv', '1947-2012lux.csv']
# csv_files = ['40cm.csv'] 

measurements = []
for file in csv_files:
    # print file,
    measurements.append(addFile(directory+file))

plot_data = [m.getDutyCycles() for m in measurements]
distances = [30, 40, 50, 60, 70, 80] #, 1705, 1947]
fontSize=20
plt.figure(figsize=(8,4))
box = plt.boxplot(plot_data, showfliers=False)
boxplot_color_fontsize(box, '#0868ac', 1.5)

# ylabels = ["{:4d}%".format(x*10) for x in ]
plt.gca().grid(True) 
plt.xticks(range(1, len(distances)+1),distances, fontsize=fontSize+2)
plt.yticks(fontsize=fontSize)
plt.ylabel("Nodes duty cycle (%)", fontsize=fontSize)
plt.xlabel("Distance from RF source", fontsize=fontSize)
plt.tight_layout()
plt.savefig('../../paper_IPSN_2020/figures/rf_cis_dutyCycle.eps')
plt.show()
