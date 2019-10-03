import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-ticks')


def main():
    
    ton = 0.1                   # nodes on-time
    tp_ref  = 1                 # power cycle length
    te = 0.01                   # event length
    num_nodes  = 10
    sim_cntr= int(1e4)          # number of iterations for single simulation

    results = []

    for i in range(1,6):
        results.append(simulate_cis_coverage(ton * i, te, tp_ref, num_nodes ,sim_cntr))
    availability = np.array(results)[:,0]  * 100 # the 100 is for plotting scale
    effective_availability = np.array(results)[:,1] * 100
    detected = np.array(results)[:,2] * 100
    captured = np.array(results)[:,3] * 100

    # effective_availability = effective_availability * num_nodes * ((ton - te)/tp_ref)**2

    print(availability) 
    print(effective_availability) 
    print(detected) 
    print(captured) 

    f = plt.figure(figsize=(8,4))

    model = [65,
            89,
            97,
            99,
            99.9]

    effective_model = [56,
            83,
            94,
            98,
            99]

    plt.plot(model, '-o', label="availability model", lw=2)
    plt.plot(availability ,'-v', label="availability") 
    plt.plot(effective_availability, '.o', label="effective availability model")
    plt.plot(effective_availability, '-*', label="effective availability")
    plt.plot(detected , '-.', label="detected events", lw=1.25)
    plt.plot(captured , ':', label="captured events", lw=1.25)

    plt.yticks(fontsize=14)
    plt.xticks([0,1,2,3,4], [10,20,30,40, 50],fontsize=14)
    plt.ylabel("(%)", fontsize=16)
    plt.xlabel("Nodes Duty Cycles (%)", fontsize=16)
    # plt.ylim([25,65])
    plt.legend(fontsize=16)
    plt.tight_layout()
    plt.savefig('../paper/figures/effective_availability.eps')
    plt.show()


def simulate_cis_coverage(ton, te, tp_ref, n, sim_cntr):
    availability=[]
    effective_availability=[]  

    detected = 0
    captured = 0
    tp = []        
    current_tp=0

    fired_events=0

    for i in range(sim_cntr):
        nodes = np.random.uniform(0,tp_ref ,n) # generate the nodes
        current_tp =max(nodes)-min(nodes)+ton  # determine the length of the current power cycle
        
        if np.random.uniform(0,1,1) < 0.1:
            continue
        else:
            fired_events+=1

        event = np.random.uniform(0,current_tp-te,1)

        tp.append(current_tp)
        # calcuate the CIS availability
        availability.append(time_span(nodes, ton))
        effective_availability.append(time_span(nodes, ton - te))

        ## Event Detection and Capturing
        # remove all the nodes that wake up after the occurance of the event
        useful_nodes = nodes[nodes < event]
        # check if there are still some nodes left
        if len(useful_nodes) < 1:
            continue
            
        dif = event - np.max(useful_nodes) 
        if dif <= ton:
            detected +=1
        if dif <= (ton - te):
            captured+=1

    return [sum(availability)/sum(tp), sum(effective_availability)/sum(tp), 
    detected/fired_events, captured/fired_events ]


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
































