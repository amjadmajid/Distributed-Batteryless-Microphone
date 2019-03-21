#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
import logicAnalyzerData as lad
import numpy as np
import matplotlib.pyplot as plt

class Plotter:

    def __init__(self, data):
        self.data = data
        self.interpolatedStates=[]
        self.interpolatedTimestamps=[] 
        self.__dataInterpolation()

    def __dataInterpolation(self):
        """This method interpolates the logic analyzer data to enable
        square-like graph plotting."""
        clustersTimestamps=[]
        timestamps=self.data[0]
        states=self.data[1]
        for idx in range(len(timestamps)-1):
            self.interpolatedTimestamps.append(timestamps[idx])
            self.interpolatedTimestamps.append(timestamps[idx+1])
            self.interpolatedStates.append(states[idx])
            self.interpolatedStates.append(states[idx])
        self.interpolatedTimestamps.append(timestamps[-1])
        self.interpolatedStates.append(states[-1])

    def plotOnTime(self, title=None):
        plt.figure()
        #print(np.sum(self.interpolatedStates, axis=1))
        plt.plot(self.interpolatedTimestamps,np.sum(self.interpolatedStates, axis=1) > 0 )

    def plotClusters(self):
        plt.figure()
        #print(np.sum(self.interpolatedStates, axis=1))
        plt.plot(self.interpolatedTimestamps,np.sum(self.interpolatedStates, axis=1))
        
    def gbar(lsts, gapSize=0.1):
        dataLen=len(lsts)
        gap=gapSize
        bw = (1-gap)/len(dataLen)
        for i in range(datalen):
            plt.bar(np.arange(len(lsts[0]))+bw*i, lsts[i], width=bw)  

