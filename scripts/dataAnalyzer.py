#
# @Author: Amjad Majid
# @Date  : March 14, 2019
#
class Analyzer:

    def __init__(self, data):
        self.timestamps= data[0]
        self.states   = data[1]
    def collectiveOnTime(self):

        dataLen=len(self.timestamps)
        onTime_start=False
        onTimeIntervals=[]

        for idx in range(dataLen):
#            print(type(self.states[idx]))
            try:
                # if single node is selected then states will be an integer
                # and cannot be summed 
                state = sum(self.states[idx])
            except TypeError:
                state = self.states[idx]
            # find the bigenning of an on-time interval
            if  state > 0 and not onTime_start:
                onTime_start=True
                onTime_stamp=self.timestamps[idx]

            # find the end of the on-time interval
            if state == 0 and onTime_start:
                onTime_start=False
                onTimeIntervals.append(self.timestamps[idx] - onTime_stamp)
        
        if onTime_start:
            onTimeIntervals.append(self.timestamps[-1] - onTime_stamp)


        #print("On time intervals", onTimeIntervals)
        return onTimeIntervals

    def collectiveOffTime(self):

        dataLen=len(self.timestamps)
        offTime_start=False
        offTimeIntervals=[]

        for idx in range(dataLen):
#            print(type(self.states[idx]))
            try:
                # if single node is selected then states will be an integer
                # and cannot be summed 
                state = sum(self.states[idx])
            except TypeError:
                state = self.states[idx]
            # find the bigenning of an on-time interval
            if  state == 0 and not offTime_start:
                offTime_start=True
                onTime_stamp=self.timestamps[idx]

            # find the end of the on-time interval
            if state > 0 and offTime_start:
                offTime_start=False
                offTimeIntervals.append(self.timestamps[idx] - onTime_stamp)
        
        if offTime_start:
            offTimeIntervals.append(self.timestamps[-1] - onTime_stamp)


        #print("Off time intervals", offTimeIntervals)
        return offTimeIntervals
    
    def getTotalTime(self):
        return self.timestamps[-1]

