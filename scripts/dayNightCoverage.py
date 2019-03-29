import matplotlib.pyplot as plt
import numpy as np

night='../data/DIS_uptime/470uf/random-initial-conditions_7-nodes_5-mins_indoor_night_March-11-2019.txt'
day='../data/DIS_uptime/470uf/random-initial-conditions_7-nodes_5-mins_no-artificial-light_windows-fully-open_cloudy-day_March-12-2019.txt'

def gbar(lsts,labels, title="Figure", gapSize=0.1):
        plt.title(title)
        dataLen=len(lsts)
        gap=gapSize
        bw = float(1-gap)/dataLen
        for i in range(dataLen):
            plt.bar(np.arange(len(lsts[0]))+bw*i, lsts[i], width=bw, label=labels[i])  
        plt.legend()


dayDutyCycle=day.replace('.txt', 'dutyCycle.txt')
nightDutyCycle=night.replace('.txt', 'dutyCycle.txt')
dc = [[float(n) for n in open(dayDutyCycle)], [float(x) for x in open(nightDutyCycle)]]
plt.figure()
gbar(dc, ["day", "night"], title="on/off duty cycle" )


plt.figure()
plt.plot([ float(n) for n in open(day)], '-*', label="day")
plt.legend()
plt.plot([ float(n) for n in open(night)], '-^', label="night")
plt.legend()
plt.xlabel("number of nodes")
plt.ylabel("availability percentage")

plt.tight_layout()
plt.show()
