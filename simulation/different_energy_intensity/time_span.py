import numpy as np
from node import Node

def main():

	nodes=[]
	num_pwr_cycles  = 10
	t_on_sunlight 	= 0.5  # t_s (or t_on) when nodes in sleep mode under sunlight
	t_off_sunlight 	= 0.5  # t_off when nodes under sunlight
	t_on_shadow 	= 0.1  # t_s (or t_on) when nodes in sleep mode in shadow
	t_off_shadow 	= 2    # t_off when nodes in shadow

	nodes_in_shadow = 0.2

	for i in np.arange(num_pwr_cycles):
		if np.random.uniform() < nodes_in_shadow:
			nodes.append(Node(num_pwr_cycles, t_on_shadow, t_off_shadow))
		else:
			nodes.append(Node(num_pwr_cycles, t_on_sunlight, t_off_sunlight))
	print(time_span(nodes))
	# for node in nodes:
	# 	print(node)


def time_span(nodes):
    span=0
    sorted_nodes = sorted(nodes, key=lambda node:node.wake_up_time)
    num_nodes 	 = len(sorted_nodes)
    print("Number of nodes: ", num_nodes)

    # removing completely overlapping nodes
    idx = 0
    while idx < num_nodes-1:
    	if (sorted_nodes[idx].wake_up_time+sorted_nodes[idx].on_time) > \
        sorted_nodes[idx+1].wake_up_time+(sorted_nodes[idx+1].on_time):
    		del sorted_nodes[idx+1] # do not advance the counter because you delete a node
    		num_nodes-=1 # reduce the total number of nodes
    		# print("Remaining number of nodes: ", num_nodes)
    	else:
    		idx+=1

    # calculate the total time span
    for i in np.arange(num_nodes-1):
        dif = sorted_nodes[i+1].wake_up_time - sorted_nodes[i].wake_up_time
        if dif > sorted_nodes[i].on_time:
        	span+=sorted_nodes[i].on_time
        else:
            span+=dif

    span+=(sorted_nodes[-1].on_time) # add the on-time of the last node
    return span

if __name__ == "__main__": 
    main()


