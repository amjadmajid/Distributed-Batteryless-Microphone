import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-ticks')

def main():

	e_harv_rate_in_shadow = 0.4   # relative to harvesting in sunlight

	ton = 0.1                   # nodes on-time
	n = 10 
	nodes_in_sunlight = int(n * 0.7)
	nodes_in_shadow = n - nodes_in_sunlight 


	observed_power_cycles_in_sunlight = int(1e4)
	# since the harvesting rate is less, the off-time is significantly longer
	observed_power_cycles_in_shadow = int(observed_power_cycles_in_sunlight * e_harv_rate_in_shadow) 


	availability=[]


	num_wake_ups = nodes_in_sunlight * observed_power_cycles_in_sunlight
	nodes = list(np.random.uniform(0,observed_power_cycles_in_sunlight ,num_wake_ups)) 
	availability.append(time_span(nodes, ton))   						# simulated availability

	# Normalization 
	availability = np.array(availability)/observed_power_cycles_in_sunlight * 100 # the 100 is for plotting scale

	# Plotting 
	f = plt.figure(figsize=(8,4))

	plt.plot(availability ,			 '-v', label="uniform energy density") 

	plt.yticks(fontsize=14)
	plt.xticks([0,1,2,3,4], [10,20,30,40, 50],fontsize=14)
	plt.ylabel("(%)", fontsize=16)
	plt.xlabel("Nodes' duty cycles (%)", fontsize=16)
	plt.legend(fontsize=16)
	plt.tight_layout()
	plt.savefig('../paper/figures/different_energy_density.eps')
	plt.show()




def time_span(intervals, on_time):
    span=0
    intervals = sorted(intervals)
    num_inters =  len(intervals)

    for i in range(num_inters-1):
        dif = intervals[i+1] - intervals[i]
        if dif < on_time:
            span+=dif
        else:
            span+=on_time

    span+=(on_time)
    return span







if __name__ == "__main__": 
    main()
































