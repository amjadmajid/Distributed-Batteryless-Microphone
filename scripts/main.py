#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
import matplotlib.pyplot as plt
import numpy as np
import sys
from fileSelector import FileSelector
from logicAnalyzerData import LogicAnalyzerData, DataException
from dataAnalyzer import Analyzer
from plotter import Plotter

np.set_printoptions(threshold=sys.maxsize)

def sysAvailable(totTime, timeInterval,nodesIndices, dataHandler):
    """ 
        Calculating the percentages of the overall on-time  of an intermittent 
        device over given intervals. This function requires the Analyzer class.

        Parameters:
        ----------
        @totTime      : int 
                        The total observation time of an experiments.
        @timeInteravl : int 
                        The granularity over which the averages on-times are 
                        calculated.
        @nodesIndices : list
                        A list of nodes indices
        @dataHandler  : instance of LogicAnalyzerData class

        Return
        ------
        availability: list
                      A list of system availabity along the specified intervals
    """
    availability=[ [] for i in nodesIndices] 
    for interval in range(0,totTime, timeInterval):
        for idx, node in enumerate(nodesIndices):
            # System availability 
            try:
                data = dataHandler.getData(interval, interval+timeInterval, range(node+1))
            except DataException as e:
                print("Error", e)
            else:
                #print("data: ", data)
                dataAnalyzer = Analyzer(data)
                collecOnTime = sum(dataAnalyzer.collectiveOnTime())
                availability[idx].append(collecOnTime / timeInterval)
    return availability

def sysDutyCycle(totTime, timeInterval,nodes, dataHandler):
    """ 
        Calculating nodes duty cycles. This function requires the Analyzer class.

        Parameters:
        ----------
        @totTime      : int 
                        The total observation time of an experiments.
        @timeInteravl : int 
                        The granularity over which an averaged duty cycle is 
                        calculated.
        @nodesIndices : list
                        A list of nodes indices
        @dataHandler  : instance of LogicAnalyzerData class

        Return
        ------
        sysDCycle: list
                    A list of nodes duty cycles
    """
    sysDCycle=[ [] for i in nodes]  
    for interval in range(0,totTime, timeInterval):
        for node in nodes:
            # System duty cycles
            data = dataHandler.getData(interval, interval+timeInterval, node)
            #print(data)
            #exit()      #### EXIT #-#--#---#----#
            dataAnalyzer = Analyzer(data)
            collecOnTime = dataAnalyzer.collectiveOnTime()
            #print(collecOnTime)
            sysDCycle[node] += collecOnTime
    return sysDCycle


def main():
    fs = FileSelector('../data/')
    path = fs.getPath()
    dataHandler = LogicAnalyzerData(path)
    numOfNodes =  dataHandler.getNumOfNodes()
    totTime=int(dataHandler.getTotalExperimentTime())+1 # seconds
    timeInterval = totTime # seconds
    timelineInterval = 10
    maxAvgSpan=[]

    availability = sysAvailable(totTime, timeInterval,range(numOfNodes), dataHandler)
    sysDutyCycles = sysDutyCycle(totTime, timeInterval,range(numOfNodes), dataHandler)
    #exit()      ##### EXIT #-#--#---#----#
    availabilityTimeline = sysAvailable(totTime, timelineInterval,[numOfNodes-1], dataHandler)
    with open("availability.txt", "w") as f:
        print(availability, file=f)

    with open("dutyCycle.txt", "w") as f:
        print(np.array(sysDutyCycles), file=f)

    with open("availabilityTimeline.txt", "w") as f:
        print(availabilityTimeline, file=f)

#------------------------Plotting------------------------------#
#    data = dataHandler.getData(0,timeInterval, range(numOfNodes))
#    plotter = Plotter(data)
#    plotter.plotClusters()
#    plotter.plotOnTime()

    plt.figure()
    plt.title("Nodes Duty Cycles")
    #print("sysDutyCycles", sysDutyCycles)
    plt.boxplot(sysDutyCycles)
#    lst=np.mean(sysDutyCycles, axis=1)
#    plt.bar(range(len(lst)),lst,)

#    fileName =path.replace('.csv', 'dutyCycle.txt')
#    #print(fileName)
#    with open(fileName,'w') as res_file:
#        for v in lst:
#            print(v,file=res_file )
    
#    for i in range(len(lst)):
#        maxAvgSpan.append(sum(lst[:i+1]))

    plt.figure()
    plt.title("system availability")
    lst=np.mean(np.array(availability), axis=1)
    fileName =path.replace('.csv', '.txt')
    #print(fileName)
    with open(fileName,'w') as res_file:
        for v in lst:
            print(v,file=res_file )

    plt.plot(range(len(maxAvgSpan)), maxAvgSpan, '-^',label='Max time Span')
    plt.legend()
    plt.plot(range(len(lst)),lst, '-*', label='on-time')
    plt.legend()

    plt.figure()
    plt.title("Availability Timeline")
    plt.plot(availabilityTimeline[0])
    plt.plot( [np.mean(availabilityTimeline[0])] * len(availabilityTimeline[0]) )
    plt.show()

if __name__=="__main__":
    main()
