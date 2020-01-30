import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-ticks')

def main():

	ton = 0.1                   # nodes on-time
	te = 0.01                   # event length
	n = 10 
	duty_cycles = range(1,6)     #  duty_cycles * ton OR duty_cycles * (ton-te)

	observed_time = int(1e4)
	num_events = observed_time
	captured=[]
	model=[]
	effective_model=[]
	availability=[]
	effective_availability=[]

	for i in duty_cycles:
		num_wake_ups = n * observed_time
		nodes = list(np.random.uniform(0,observed_time ,num_wake_ups)) 
		events = list(np.random.uniform(0,observed_time,num_events))

		availability.append(time_span(nodes, ton*i))   						# simulated availability
		effective_availability.append(time_span(nodes, (ton-te) *i))		# simulated effective availability

		captured.append(captured_events(nodes, events, (ton-te)*i,te))
		
		model.append(tot(n, ton*i))
		effective_model.append(tot(n, (ton-te)*i))

	# Normalization 
	availability = np.array(availability)/observed_time * 100 # the 100 is for plotting scale
	effective_availability = np.array(effective_availability)/observed_time * 100
	model = np.array(model) * 100
	effective_model = np.array(effective_model) * 100
	captured = np.array(captured)/num_events * 100

	# Plotting 
	f = plt.figure(figsize=(8,4))

	plt.plot(model, 				 '-o', label="(modeled) availability", lw=2)
	plt.plot(availability ,			 '-v', label="(simulated) availability") 
	plt.plot(effective_model, 		 ':o', label="(modeled) effective availability", lw=2)
	plt.plot(effective_availability, ':*', label="(simulated) effective availability",lw=2)
	plt.plot(captured , 			 '-.', label="(simulated) captured events", lw=2)

	plt.yticks(fontsize=14)
	plt.xticks([0,1,2,3,4], [10,20,30,40, 50],fontsize=14)
	plt.ylabel("(%)", fontsize=16)
	plt.xlabel("Nodes' duty cycles (%)", fontsize=16)
	plt.legend(fontsize=16)
	plt.tight_layout()
	plt.savefig('../paper/figures/effective_availability.eps')
	plt.show()


def tot(n,ndc):
	"""The modeled CIS availability"""
	assert (n >0 and ndc <= 1)
	t=0
	coverage=[]
	for i in range(n):
		#t = (1 - t) * (np.random.randn() * (ndc/4.) + ndc) +t
		t = t + (1 - t) * ndc
		if i == n-1:  # the coverage at certain number of nodes
			# print(t)
			coverage.append(t)
	return coverage

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


def captured_event(e, te, node, effective_ton):
	"""captured_event assumes that the node wakes up before the event"""
	if (e >= node) and ((e - node) <= (effective_ton)): # the time difference between the moment
								#  at which a node powers up and an event
								# happens must be larger than the effective
								# on-time
		# print((e - node), (ton - te) )
		return True
	return False

def captured_events(nodes, events, ton, te):
	captured=0
	
	nodes =  sorted(nodes, reverse=True)
	events = sorted(events, reverse=True)

	nodes = np.array(nodes)
	useful_nodes = nodes[nodes <= events[0]]
	if len(useful_nodes)<1:
		return captured

	useful_nodes = list(useful_nodes)

	# print("useful_nodes", useful_nodes)

	for event in events:
		while len(useful_nodes) > 0:
			if captured_event(event, te, useful_nodes[0], ton):
				captured+=1
				break   # this node might capture a new event
			elif event > useful_nodes[0]:
				break  # event undetectable. The node might capture new event
			else:
				del useful_nodes[0]  # the node powered up after the event, it must be removed

	return  captured





if __name__ == "__main__": 
    main()
































