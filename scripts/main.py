#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
import logicAnalyzerData as lad
import dataAnalyzer as da
import plotter as p
import matplotlib.pyplot as plt
import numpy as np

#path = '../data/DIS_uptime/680uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-30-percent-open_cloudy-day_March-12-2019.csv'
#path='../data/DIS_uptime/680uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-fully-open_cloudy-day_March-12-2019.csv'
path='../data/DIS_uptime/680uf/random-initial-conditions_8-nodes_5-mins_with-artificial-light_windows-fully-open_night_March-12-2019.csv'

#path='../data/DIS_uptime/random-initial-conditions_7-nodes_5-mins_indoor_night_March-11-2019.csv'
#path='../data/DIS_uptime/random-initial-conditions_7-nodes_5-mins_no-artificial-light_windows-fully-open_cloudy-day_March-12-2019.csv'

def sysAvailable(totTime, timeInterval,nodes, dataHandler, da):
    availability=[ [] for i in range(nodes)] 
    for interval in range(0,totTime, timeInterval):
        for node in range(nodes):
            # System availability 
            data = dataHandler.getData(interval, interval+timeInterval, range(node+1))
            dataAnalyzer = da.Analyzer(data)
            collecOnTime = sum(dataAnalyzer.collectiveOnTime())
            availability[node].append(collecOnTime / timeInterval)
    return availability

def sysDutyCycle(totTime, timeInterval,nodes, dataHandler, da):
    sysDCycle=[ [] for i in range(nodes)]  
    for interval in range(0,totTime, timeInterval):
        for node in range(nodes):
            # System duty cycles
            data = dataHandler.getData(interval, interval+timeInterval, node)
            dataAnalyzer = da.Analyzer(data)
            collecOnTime = sum(dataAnalyzer.collectiveOnTime())
            sysDCycle[node].append(collecOnTime / timeInterval)
    return sysDCycle

def main():

    dataHandler = lad.LogicAnalyzerData(path)
    nodes =  dataHandler.getNumOfNodes()
    totTime=int(dataHandler.getTotalExperimentTime())+1 # seconds
    timeInterval = totTime # seconds
    timelineInterval = 10
    availabilityTimeline = []

    availability = sysAvailable(totTime, timeInterval,nodes, dataHandler, da)
    sysDutyCycles = sysDutyCycle(totTime, timeInterval,nodes, dataHandler, da)

            
    # Availability time line for a certain interval and number of nodes
    for interval in range(timelineInterval,totTime+timelineInterval, timelineInterval):
            data = dataHandler.getData(interval-timelineInterval,interval, range(nodes))
            dataAnalyzer = da.Analyzer(data)
            collecOnTime = sum(dataAnalyzer.collectiveOnTime())
            availabilityTimeline.append(collecOnTime / timelineInterval)
    
#------------------------Plotting------------------------------#
    data = dataHandler.getData(0,timeInterval, range(nodes))
    plotter = p.Plotter(data)
    plotter.plotClusters()
    plotter.plotOnTime()

    plt.figure()
    plt.title("Nodes Duty Cycles")
    lst=np.mean(sysDutyCycles, axis=1)
    plt.bar(range(len(lst)),lst)
    maxAvgSpan=[]
    for i in range(len(lst)):
        maxAvgSpan.append(sum(lst[:i+1]))
    plt.figure()
    plt.title("System Availability")
    lst=np.mean(np.array(availability), axis=1)
    #print(lst)
    plt.bar(range(len(maxAvgSpan)), maxAvgSpan)
    plt.bar(range(len(lst)),lst)

    plt.figure()
    plt.title("Availability Timeline")
    plt.plot(availabilityTimeline)
    plt.show()


if __name__=="__main__":
    main()
