from inspect import currentframe, getframeinfo
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd

plt.style.use('seaborn-ticks')

data = pd.read_csv("../processed_data/BatterylessNodesDutyCycles_Active_mode.csv")
# print( data.to_string())

fig = plt.figure(figsize=(8,4))
plt.plot(data['Energy Intensity (lux)'], data['On-time'], '-^')
plt.plot(data['Energy Intensity (lux)'], data['Off-time'], '-v')
plt.plot(data['Energy Intensity (lux)'], data['Power Cycle Length'], '-o')


fontSize = 18 
plt.ylabel("Time (seconds)", fontsize=fontSize)
plt.xlabel("Energy Intensity (lux)", fontsize=fontSize)
# plt.xticks(np.arange(5)+1,(300,500,800,1000,1400),fontsize=fontSize-2)
plt.yticks(fontsize=fontSize-2)
plt.xticks(fontsize=fontSize-2)
plt.tight_layout()
plt.savefig('../../paper/figures/BatterylessNodesDutyCycles_Active_mode.eps')



data = pd.read_csv("../processed_data/BatterylessNodesDutyCycles_Sleep_mode.csv")
# print( data.to_string())

fig = plt.figure(figsize=(8,4))
plt.plot(data['Energy Intensity (lux)'], data['On-time'], '-^')
plt.plot(data['Energy Intensity (lux)'], data['Off-time'], '-v')
plt.plot(data['Energy Intensity (lux)'], data['Power Cycle Length'], '-o')


fontSize = 18 
plt.ylabel("Time (seconds)", fontsize=fontSize)
plt.xlabel("Energy Intensity (lux)", fontsize=fontSize)
# plt.xticks(np.arange(5)+1,(300,500,800,1000,1400),fontsize=fontSize-2)
plt.yticks(fontsize=fontSize-2)
plt.xticks(fontsize=fontSize-2)
plt.tight_layout()
plt.savefig('../../paper/figures/BatterylessNodesDutyCycles_Sleep_mode.eps')


plt.show()
    
# if __name__=="__main__":
#     main()