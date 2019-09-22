#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
import re
import json
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
                #print("collectOntime", collecOnTime)
                availability[idx].append(collecOnTime / timeInterval)
    return availability

def intermittent_nodes_offtimes(totTime, timeInterval,nodes, dataHandler):
    """ 
        Calculating nodes off-times. This function requires the Analyzer class.

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
                    A list of nodes off-times 
    """
    offTimes=[ [] for i in nodes]  
    for interval in range(0,totTime, timeInterval):
        for node in nodes:
            # System duty cycles
            data = dataHandler.getData(interval, interval+timeInterval, node)
            #print(data)
            #exit()      #### EXIT #-#--#---#----#
            dataAnalyzer = Analyzer(data)
            collecOffTime = dataAnalyzer.collectiveOffTime()
            #print(collecOnTime)
            offTimes[node] += collecOffTime
    return offTimes 

def intermittent_nodes_ontimes(totTime, timeInterval,nodes, dataHandler):
    """ 
        Calculating nodes on-times. This function requires the Analyzer class.

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
                    A list of nodes on-times 
    """
    onTimes=[ [] for i in nodes]  
    for interval in range(0,totTime, timeInterval):
        for node in nodes:
            # System duty cycles
            data = dataHandler.getData(interval, interval+timeInterval, node)
            #print(data)
            #exit()      #### EXIT #-#--#---#----#
            dataAnalyzer = Analyzer(data)
            collecOnTime = dataAnalyzer.collectiveOnTime()
            #print(collecOnTime)
            onTimes[node] += collecOnTime
    return onTimes 

def labelFinder(path, pattern):
    """LabelFinder extracts label from the file name. It looks for the labels
    `night`, `day`, `cloudy`, and `sunny` with some other descriptive words 
    
    @param  : str
              File name
    """
    try:
        label = re.search(pattern, path).group()
        print("label", label)
    except AttributeError as e:
        print("label is not found")
        print()
        print(e)
        try:
            label = label.replace("_", " ")
        except UnboundLocalError:
            pass
        try:
            label = label.replace("-", " ")
        except UnboundLocalError:
            pass

    return label

def main():
    fs = FileSelector('../data/')
    path = fs.getPath()
    print(path)
    labelPattern = "(_?[s|S]unny_?|_?[D|d]ay_?|_?[N|n]ight_?|_?cloudy.*?_|[C|c]loudy|[0-9]*-?[0-9]+(lux|cm))"
    label = labelFinder(path, labelPattern)
    print(label)
    capPattern = "220|470|680|1000|RF"
    cap = labelFinder(path, capPattern)
    print(cap)
        
    dataHandler = LogicAnalyzerData(path)
    numOfNodes =  dataHandler.getNumOfNodes()

    # clus_tim, clus = dataHandler.getClusters()
    # jsonObj = json.dumps([label,clus.tolist()])
    # with open("processed_data/clusters_rf.json", "a") as f:
    #     print(jsonObj, file=f)
    # exit()

    totTime=int(dataHandler.getTotalExperimentTime())+1 # seconds
    timeInterval = totTime # seconds
    timelineInterval = 10
    
    availability = sysAvailable(totTime, timeInterval,range(numOfNodes), dataHandler)
    nodesOnTimes = intermittent_nodes_ontimes(totTime, timeInterval,range(numOfNodes), dataHandler)
    nodesOffTimes = intermittent_nodes_offtimes(totTime, timeInterval,range(numOfNodes), dataHandler)
    # interpolate the data according to the given interval
    dataHandler.intervalDataInterpolation(timelineInterval)
    availabilityTimeline = sysAvailable(totTime, timelineInterval,[numOfNodes-1], dataHandler)

    jsonObj = json.dumps([label,availability])
    #TODO prevent duplicated entries
    with open("processed_data/availability"+cap+".json", "a") as f:
        print(jsonObj, file=f)

    jsonObj = json.dumps([label,nodesOnTimes])
    with open("processed_data/intermittent_nodes_ontimes"+cap+".json", "a") as f:
        print(jsonObj, file=f)

    jsonObj = json.dumps([label,nodesOffTimes])
    with open("processed_data/intermittent_nodes_offtimes"+cap+".json", "a") as f:
        print(jsonObj, file=f)

    jsonObj = json.dumps([label,availabilityTimeline])
    with open("processed_data/availabilityTimeline"+cap+".json", "a") as f:
        print(jsonObj, file=f)

    plt.figure()
    plt.title("Availability Timeline")
    plt.plot(availabilityTimeline[0], '-*')
    plt.plot( [np.mean(availabilityTimeline[0])] * len(availabilityTimeline[0]) )
    plt.show()

if __name__=="__main__":
    main()
