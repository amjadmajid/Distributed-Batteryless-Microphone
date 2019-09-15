#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
import csv
import numpy as np

class DataException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class LogicAnalyzerData:
    """This class requires a csv file of time stamped binary states,
    like files generated from Saleae logic analyzer. It extracts the 
 i   rows within the given time interval, and it selects the states 
    columns based on the given list of columns' indices. 
    """

    def __init__(self,path):
        self.path = path
        self.timestamps=[]
        self.states=[]

        self.__readData()

    def __readData(self):
        with open(self.path) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')

            # If there is a header line drop it, otherwise rewind your file pointer 
            line = csvReader.__next__()
            if 'Time' not in line[0]:
                csvFile.seek(0,0)

            for line in csvReader:
                self.states.append(list(map(int, line[1:])))
                self.timestamps.append(float(line[0])) 
            print(len(self.states))

    def __timeRange(self,minTimestamp, maxTimestamp):
        """ __timeRane(...) time range selector [...)

            @param `minTimestamp` is the lower bound of the time interval. This bound is included  
            @param `maxTimestamp` is the upper bound of the time interval. This bound is exculded 
            @return `rowsIndices` is a list of row indices of the data within the given time interval
        """
        #TODO to optimize this method find the beginning of the time interval using binary search
        rowsIndices = [self.timestamps.index(ts) for ts in self.timestamps \
                if ts >= minTimestamp and ts <= maxTimestamp]
        #print(rowsIndices)
        if not rowsIndices:
            raise DataException("Not data in the found between {} and {}".format(minTimestamp, maxTimestamp))
        return rowsIndices 

    def statesSelector(self, cols, states):
        s = np.array(states)
        # print(s)
        # print("cols",cols)
        return s[:,cols]

    def getNumOfNodes(self):
        return len(self.states[0])

    def getTotalExperimentTime(self):
        return self.timestamps[-1]

    def getData(self, minTime, maxTime, cols):
        # print("minMax",minTime,maxTime)
        indices = self.__timeRange(minTime, maxTime)
        # print("indices",indices)
        rawStates = [ self.states[i] for i in indices]
        # print("rawStates", rawStates)
        timestamps = np.array([ self.timestamps[i] for i in indices])
        states = self.statesSelector(cols,rawStates)
        #print("getData->states", states)
        return timestamps, states

    # for debugging
    def displayFileData(self):
        for idx in range(len(self.timestamps)):
            print(self.timestamps[idx], self.states[idx])

    def intervalDataInterpolation(self,interval):
        timespan=interval
        if interval < 1:
            raise ValueError("interval must be greater than 0")
        timestamps=[]
        states=[]
        idx = 0
        while idx < len(self.timestamps):
            if self.timestamps[idx] == timespan:
                # we do not need to do anyting
                timestamps.append(self.timestamps[idx])
                states.append(self.states[idx])
                timespan += interval
                idx+=1

            elif self.timestamps[idx] > timespan:
                # inject an entry 
                timestamps.append(timespan)
                states.append(self.states[idx-1])
                timespan += interval
                # do not increase the index to check the entry on the entry
                # against the new interval
            else:
                timestamps.append(self.timestamps[idx])
                states.append(self.states[idx])
                idx+=1
        self.timestamps  = timestamps
        self.states = states
        #return timestamps, states

                
    def getClusters(self):
        #print(self.states)
        return np.array(self.timestamps), np.sum(self.states, axis=1)






