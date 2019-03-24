#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
import matplotlib.pyplot as plt
import numpy as np

from logicAnalyzerData import LogicAnalyzerData
from dataAnalyzer import Analyzer
from plotter import Plotter

## 470uf
path='../data/DIS_uptime/random-initial-conditions_7-nodes_5-mins_indoor_night_March-11-2019.csv'
path='../data/DIS_uptime/random-initial-conditions_7-nodes_5-mins_no-artificial-light_windows-fully-open_cloudy-day_March-12-2019.csv'

## 680uf
#path = '../data/DIS_uptime/680uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-30-percent-open_cloudy-day_March-12-2019.csv'
#path='../data/DIS_uptime/680uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-fully-open_cloudy-day_March-12-2019.csv'
#path='../data/DIS_uptime/681uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-fully-open_night_March-12-2019.csv'
#path='../data/DIS_uptime/680uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-fully-open_cloudy-near-sunset_March-15-2019.csv'

## 1000uf
#path='../data/DIS_uptime/1000uf/random-initial-conditions_3-nodes_5-mins_indoor_night_March-13-2019.csv'


night='../data/DIS_uptime/random-initial-conditions_7-nodes_5-mins_indoor_night_March-11-2019.txt'
day='../data/DIS_uptime/random-initial-conditions_7-nodes_5-mins_no-artificial-light_windows-fully-open_cloudy-day_March-12-2019.txt'

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
            data = dataHandler.getData(interval, interval+timeInterval, range(node+1))
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
            dataAnalyzer = Analyzer(data)
            collecOnTime = sum(dataAnalyzer.collectiveOnTime())
            sysDCycle[node].append(collecOnTime / timeInterval)
    return sysDCycle

def gbar(lsts,labels, title="Figure", gapSize=0.1):
        plt.title(title)
        dataLen=len(lsts)
        gap=gapSize
        bw = float(1-gap)/dataLen
        for i in range(dataLen):
            plt.bar(np.arange(len(lsts[0]))+bw*i, lsts[i], width=bw, label=labels[i])  
        plt.legend()

def main():

    dataHandler = LogicAnalyzerData(path)
    numOfNodes =  dataHandler.getNumOfNodes()
    totTime=int(dataHandler.getTotalExperimentTime())+1 # seconds
    timeInterval = totTime # seconds
    timelineInterval = 30
    maxAvgSpan=[]

    availability = sysAvailable(totTime, timeInterval,range(numOfNodes), dataHandler)
    sysDutyCycles = sysDutyCycle(totTime, timeInterval,range(numOfNodes), dataHandler)
    availabilityTimeline = sysAvailable(totTime, timelineInterval,[numOfNodes-1], dataHandler)

#------------------------Plotting------------------------------#
    data = dataHandler.getData(0,timeInterval, range(numOfNodes))
    plotter = Plotter(data)
    plotter.plotClusters()
    plotter.plotOnTime()

    plt.figure()
    plt.title("Nodes Duty Cycles")
    lst=np.mean(sysDutyCycles, axis=1)
    plt.bar(range(len(lst)),lst,)
    fileName =path.replace('.csv', 'dutyCycle.txt')
    #print(fileName)
    with open(fileName,'w') as res_file:
        for v in lst:
            print(v,file=res_file )
    
    for i in range(len(lst)):
        maxAvgSpan.append(sum(lst[:i+1]))

    plt.figure()
    plt.title("system availability")
    lst=np.mean(np.array(availability), axis=1)
    fileName =path.replace('.csv', '.txt')
    print(fileName)
    with open(fileName,'w') as res_file:
        for v in lst:
            print(v,file=res_file )

    plt.plot()
    plt.plot([ float(n) for n in open(day)], '-*', label="day")
    plt.legend()
    plt.plot([ float(n) for n in open(night)], '-^', label="night")
    plt.legend()
    plt.xlabel("number of nodes")
    plt.ylabel("availability percentage")
    #plt.plot(range(len(maxAvgSpan)), maxAvgSpan, '-^',label='Max time Span')
    #plt.legend()
    #plt.plot(range(len(lst)),lst, '-*', label='on-time')
    #plt.legend()
    
    dayDutyCycle=day.replace('.txt', 'dutyCycle.txt')
    nightDutyCycle=night.replace('.txt', 'dutyCycle.txt')
    dc = [[float(n) for n in open(dayDutyCycle)], [float(x) for x in open(nightDutyCycle)]]
    plt.figure()
    gbar(dc, ["day", "night"], title="on/off duty cycle" )

    plt.figure()
    plt.title("Availability Timeline")
    plt.plot(availabilityTimeline[0])
    plt.plot( [np.mean(availabilityTimeline[0])] * len(availabilityTimeline[0]) )
    plt.show()


if __name__=="__main__":
    main()
