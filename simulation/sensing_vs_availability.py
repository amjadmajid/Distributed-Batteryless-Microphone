import numpy as np
import matplotlib.pyplot as plt


def main():
    
    ton = 0.1                   # nodes on-time
    tp  = 1                     # power cycle length
    te = 0.01                   # event length
    num_nodes  = 10
    sim_cntr= int(1e6)          # number of iterations for single simulation
    
    simulate_cis_coverage(ton, te, tp, num_nodes ,sim_cntr)


def simulate_cis_coverage(ton, te, tp, n, sim_cntr):
    availability=[]
    effective_availability=[]       #  
    captured = 0
    
    for i in range(sim_cntr):
        nodes = np.random.uniform(0,tp - ton,n)
        event = np.random.uniform(0,tp,1)
        # calcuate the CIS availability
        availability.append(time_span(nodes, ton))
        effective_availability.append(time_span(nodes, ton - te))
        # remove all the nodes that wake up after the occurance of the event
        useful_nodes = nodes[nodes < event]
        # check if there are still some nodes left
        if len(useful_nodes) < 1:
            continue
            
        dif = event - np.max(useful_nodes) 
        if dif <= (ton - te):
            captured+=1

    print("availability = ", sum(availability)/sim_cntr)
    print("effective availability = ", sum(effective_availability)/sim_cntr)
    print("Captured events = ", captured/sim_cntr)
    print("Uncaptured events = ", 1-captured/sim_cntr )


def time_span(intervals, on_time):
    span=0
    intervals.sort()
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
































