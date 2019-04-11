import sys
sys.path.insert(0, '../')
from logicAnalyzerData import *
import matplotlib.pyplot as plt
import numpy as np
import sys, os

plt.style.use('seaborn-whitegrid')

class Coverage():
    minRecLen = 0.284
    maxRecDelay = 0.05

    def __init__(self, filename, poweredNode):
        self.filename = filename
        self.data = LogicAnalyzerData(filename)
        self.num_nodes = self.data.getNumOfNodes()
        self.poweredNode = poweredNode
        self.poweredEvents = self.__getEvents(poweredNode)  # Select the reference node on continuous power
        self.numPoweredEvents = len(self.poweredEvents)
        self.captured = [0 for i in range(self.numPoweredEvents)]
        self.detected = [0 for i in range(self.numPoweredEvents)]
        self.numLateRec = 0

        # do matching of node to powered node here
        self.detectionTot = []
        self.detection4 = []
        self.coverageTot = []
        self.coverage4 = []

        for node in range(0, self.num_nodes):
            if node != self.poweredNode:
                events = self.__getEvents(node)
                self.__match(events)

                self.detectionTot.append( 100 * sum(self.getDetectedCoverage()) / float(self.numPoweredEvents) )
                self.detection4.append( 100 * sum(self.getDetectedCoverage()[:4]) / 4.0)

                self.coverageTot.append( 100 * sum(self.getCapturedCoverage()) / float(self.numPoweredEvents) )
                self.coverage4.append( 100 * sum(self.getCapturedCoverage()[:4]) / 4.0)


    def __match(self, nodeEvents):
        for event in nodeEvents:
            for i in range(len(self.poweredEvents)):
                if (abs(event[0]-self.poweredEvents[i][0]) < self.maxRecDelay):
                    if (event[1]-event[0] > self.minRecLen):
                        self.captured[i] +=1
                        self.detected[i] +=1
                        break
                    else:
                        self.detected[i] +=1
            else:            
                # If does not fit to any poweredEvent
                if (event[1]-event[0] > self.minRecLen):         
                    self.numLateRec +=1

    def __getEvents(self, node, start_time=0, end_time=-1):
        """
        Extracts events (recording) from single node data
        """
        if type(node) != int:
            raise Exception("Select 1 node please")

        if end_time == -1:
            end_time = self.data.getTotalExperimentTime()

        data = self.data.getData(start_time, end_time,[node])
        events = []
        state = data[1][0]

        if state == 1: # If state is already high when measurement started, don't count
            start = 0

        for i in range(len(data[0])):
            if state == 0:
                if data[1][i] == 1:
                    start = data[0][i]
                    state = 1

            if state == 1:
                if data[1][i] == 0:
                    if start != 0: # If state is already high when measurement started, don't count
                        stop = data[0][i]
                        events.append( (start,stop) )
                    state = 0

        return events



    def getCaptured(self):
        return self.captured

    def getCapturedCoverage(self):
        return [0 if x == 0 else 1 for x in self.captured]

    def getDuplicateCapture(self):
        return 100* sum([0 if x < 2 else 1 for x in self.captured])  / float(self.numPoweredEvents)

    def getSingleCapture(self):
        return [1 if x == 1 else 0 for x in self.captured]

    def getDetected(self):
        return self.detected

    def getDetectedCoverage(self):
        return [0 if x == 0 else 1 for x in self.detected]

    def getDuplicateDetection(self):
        return 100* sum([0 if x < 2 else 1 for x in self.detected]) / float(self.numPoweredEvents)

    def getSingleDetection(self):
        return [1 if x == 1 else 0 for x in self.detected]

    def plot(self):
            plt.bar(range(len(self.captured)),self.captured)
            plt.show()


def processCoverage(filename):
    cov = Coverage(filename, 8)

    # return [cov.detectionTot[-1], cov.coverageTot[-1], cov.getDuplicateDetection() ,cov.getDuplicateCapture()]
    return [sum(cov.getDetected()), sum(cov.getDetectedCoverage())]


# def sliceMultiBurst(filename):


def plotBarGraph(labels, data):
    """
    data in the form [ [value1, value2, ..], [value1, ..] ]
    """
    fontSize=16
    f = plt.figure(figsize=(8,4))

    data= np.transpose(data)
    print (data)
    # color_list = ["#edf8e9" , '#bae4b3', '#74c476', '#31a354', '#006d2c']
    color_list = [ '#bae4b3',   '#31a354']
    gap = .1
    bw = (1-gap)/(len(data)/2)
    for i in range(len(data)):
        plt.bar(np.arange(len(data[0])) +bw*(i//2), data[i], width=bw, color=color_list[i], tick_label=labels)

    plt.legend(["Total events", "Unique events"], loc="upper left", fontsize=fontSize)
    plt.xticks(fontsize=fontSize-2)
    plt.yticks(fontsize=fontSize-2)
    plt.xlabel('Light intensity (lux)', fontsize=fontSize)
    plt.ylabel('Number of events', fontsize=fontSize)
    plt.tight_layout()
    plt.savefig('../../paper/figures/events_detection_rate.eps')
    plt.show()


if __name__ == '__main__':

    # filename = sys.argv[1]

    #### For regular events  
    directory = "../../data/regular_repeating_events/"
    # print "Filename, Detection_coverage, Capture_coverage, Clustered_detections, Clustered_captures"

    labels = []
    measurements = []
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    csv_files.reverse()
    for filename in csv_files:
        labels.append( int( int(filename.split("-")[0])/100) * 100) 
        measurements.append(processCoverage(directory+filename))

    plotBarGraph(labels, measurements)

