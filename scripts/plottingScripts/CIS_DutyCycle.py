import sys
sys.path.insert(0, '../')
from logicAnalyzerData import *
import matplotlib.pyplot as plt
import numpy as np
import sys, os

plt.style.use('seaborn-whitegrid')

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
        return duty_cycle


def addFile(filename):
    m = Measurement()
    data = LogicAnalyzerData(filename)
    timestamps = data.timestamps

    for nodeNum in range(data.getNumOfNodes()):
        states = data.statesSelector([nodeNum], data.states)
        off_times = []
        on_times = []
        last_state = states[0]
        last_timestamp = timestamps[0]

        for i in range(1, len(timestamps)):
            if last_state != states[i]:
                if last_state == 0:
                    off_times.append(timestamps[i]-last_timestamp)
                    last_timestamp = timestamps[i]
                    last_state = states[i]
                if last_state == 1:
                    on_times.append(timestamps[i]-last_timestamp)
                    last_timestamp = timestamps[i]
                    last_state = states[i]

        if last_state == 0:
            off_times.append(300-last_timestamp)  # TODO make the code work also for different recording times.
        if last_state == 1:
            on_times.append(300-last_timestamp)

        n = Node(on_times, off_times)
        m.addNode(n)

    # print m.getDutyCycles()
    return m


directory = "../../data/duty_cycle_sleeping/470uf/"
# csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
csv_files = ['116-120lux.csv', '215-224lux.csv', '320-332lux.csv', '430-442lux.csv', '524-541lux.csv', '621-641lux.csv', '715-740lux.csv', '812-836lux.csv', '904-932lux.csv', '1009-1032lux.csv', '1096-1126lux.csv', '1185-1220lux.csv', '1280-1321lux.csv', '1400-1436lux.csv'] #, '1705-1737lux.csv', '1947-2012lux.csv']
measurements = []
for file in csv_files:
    # print file,
    measurements.append(addFile(directory+file))

plot_data = [m.getDutyCycles() for m in measurements]
light_intensities = [116, 215, 320, 430, 524, 621, 715, 812, 904, 1009, 1096, 1185, 1280, 1400] #, 1705, 1947]
fontSize=16
plt.figure(figsize=(8,4))
plt.boxplot(plot_data, positions=light_intensities, widths=30)

# ylabels = ["{:4d}%".format(x*10) for x in ]
plt.xticks(rotation=90, fontsize=fontSize-4)
plt.yticks(fontsize=fontSize-4)
plt.ylabel("Avg. nodes duty cycle (%)", fontsize=fontSize)
plt.xlabel("Light intensity (lux)", fontsize=fontSize)
# plt.ylim(0,1.05)
plt.xlim(0, light_intensities[-1]+50)
plt.tight_layout()
plt.savefig('../../paper/figures/cis_dutyCycle.eps')
plt.show()
