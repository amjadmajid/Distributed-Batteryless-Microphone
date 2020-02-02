import numpy as np
from node import Node


# observation_time
# pwr_cycle
# num_pwr_cycles = observation_time/pwr_cycle

def main():

	for percentage_idx in range(11):
		tot_events=[]
		cap_events=[]
		uniq_events=[]
		re=[]
		for i in range(100):
			nodes=[]
			num_nodes = 10
			cis_pwr_cycles  = 20
			num_events = cis_pwr_cycles
			nodes_in_shadow = 0.1 * percentage_idx  # the percetage of nodes in shadow
			
			t_on_sunlight 	= 0.2 * num_nodes  # t_s (or t_on) when nodes in sleep mode under sunlight
			t_off_sunlight 	= 0.8 * num_nodes  # t_off when nodes under sunlight
			t_on_shadow 	= 0.05 * num_nodes # t_s (or t_on) when nodes in sleep mode in shadow
			t_off_shadow 	= 0.95 * num_nodes # t_off when nodes in shadow
			
			max_wake_up_time = num_nodes * cis_pwr_cycles
			response_redundancy =  1

			for i in np.arange(max_wake_up_time):
				if np.random.uniform() < nodes_in_shadow:
					nodes.append(Node(max_wake_up_time, t_on_shadow, t_off_shadow))
				else:
					nodes.append(Node(max_wake_up_time, t_on_sunlight, t_off_sunlight))

			events = list(np.random.uniform(0,max_wake_up_time,num_events))


			# print("Total number events: ", len(events))
			# print("Total number of nodes: ", len(nodes))
			e = captured_events(num_nodes,nodes, events,response_redundancy)
			tot_events.append(e[0])
			cap_events.append(e[1])
			uniq_events.append(e[2])
			if e[3] not in re:
				re.append(e[3])

			# print(percentage_idx * nodes_in_shadow )
		print("nodes in shadow: ", nodes_in_shadow)
		print(np.mean(tot_events),np.mean(cap_events),np.mean(uniq_events) )
		print(re)
		print()

def cis_availability(n,ndc):
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
			availability = sum(coverage)
			# print("availability", availability)
	return availability

def active_nodes(num_nodes, node,ndc):
	"""Calculate the number of active nodes"""
	avail = cis_availability(num_nodes,ndc)
	t_max = num_nodes * node.get_on_time()
	num_active_nodes = t_max / ((node.get_on_time() + node.get_off_time()) * avail)
	# print("Number of active nodes ", num_active_nodes)
	return num_active_nodes

def response_probability(redundancy_factor, num_active_nodes):
	if redundancy_factor/num_active_nodes > 1:
		return 1
	return redundancy_factor/num_active_nodes


def captured_event(e, node):
	"""captured_event assumes that the node wakes up before the event"""
	if (e >= node.wake_up_time) and ((e <= node.wake_up_time + node.on_time)): 
		return True
	return False

def captured_events(num_nodes, nodes, events,response_redundancy ):
	captured_cnt=0   # number of captured events counter
	captured_cnt_tot=0
	captured_cnt_unique=0
	capture_flag=False
	nodes =  sorted(nodes, key=lambda node:node.wake_up_time, reverse=True)
	events = sorted(events, reverse=True)

	# for j, node in enumerate(nodes):
	# 	if j%10 == 0:
	# 		print (events[int(j/10)])
	# 	print(node)

	node_max_on_time = max(nodes, key=lambda node:node.on_time)
	max_on_time = node_max_on_time.get_on_time()

	# for i in range(len(events)):
	# 	print(nodes[i],' | ', events[i])

	i=0
	for node in nodes:
		if node.wake_up_time > events[0]: # if a node wakes up after the last event 
										  # then it is useless
			i+=1
			continue
		break
	useful_nodes = nodes[i:]
	# print("Number of removed nodes: ", len(nodes) - len(useful_nodes))

	if len(nodes)<1:
		return captured_cnt

	# Check how many nodes have captured an event
	for event in events:
		capture_flag=True
		for idx in range(len(useful_nodes)):
			node = useful_nodes[idx]
			if captured_event(event, node) :
				captured_cnt_tot+=1
				#determining the response probability
				ndc = node.get_on_time() / (node.get_on_time() + node.get_off_time())
				n_active = active_nodes(num_nodes, node, ndc)
				p_response = response_probability(response_redundancy,n_active)
				# print("the response probability is ", p_response)
				if(np.random.uniform() < p_response):
					captured_cnt+=1
					if capture_flag:
						captured_cnt_unique+=1
						capture_flag=False
			if node.wake_up_time+max_on_time < event:
				break

	return   captured_cnt_tot, captured_cnt, captured_cnt_unique, p_response



if __name__ == "__main__": 
    main()
