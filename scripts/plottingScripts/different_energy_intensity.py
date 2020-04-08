import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-ticks')


data = pd.read_csv("../../data/simulated_data/different_energy_intensity.csv", delimiter=",")
data.head()

detected_events = data.iloc[:, 0]
captured_events = data.iloc[:, 1]
unique_events   = data.iloc[:, 2]

f = plt.figure(figsize=(8,4))
fontSize=20
plt.plot(detected_events, '-o', label="detected events")
plt.plot(captured_events, '->' , label="captured events")
plt.plot(unique_events, '-^', label="uniquely captured events")
plt.xticks(fontsize=fontSize)
plt.yticks(fontsize=fontSize)
plt.ylabel("Number of events", fontsize=fontSize)
plt.xlabel("Nodes in shadow", fontsize=fontSize)
plt.legend(fontsize=fontSize)

plt.tight_layout()
plt.savefig('../../paper_IPSN_2020/figures/different_energy_intensity.eps')
plt.show()
