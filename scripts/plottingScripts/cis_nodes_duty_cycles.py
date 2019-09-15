from inspect import currentframe, getframeinfo
import numpy as np
import matplotlib.pyplot as plt
import json
plt.style.use('seaborn-ticks')

# To disable debugging set it to False
# To print all debugging info set the second entry to 0
# To print a specific message set its id
DEBUG = [False, 70]

def print_debug_info(label,msg, id):
    if DEBUG[0]:
        if DEBUG[1] == 0 or DEBUG[1] == id:
            print(label)
            print(msg)

def load_cis_data(path):
    data=[]
    with open(path) as f:
        for cis in f:
            print_debug_info("+++ cis len", len(cis),  getframeinfo(currentframe()).lineno)
            data.append(json.loads(cis))
    return data

def serialize_data(data):
    serialized_data=[]
    for cis in data:
        for node in cis:
            for val in node:
                serialized_data.append(val) 
    return serialized_data

def get_labels(data):
    return __get_column(data,0)

def get_unlabelled_data(data):
    return __get_column(data,1)

def __get_column(data,idx):
    col=[]
    for row in data:
        col.append(row[idx])
    return col

def __get_the_smaller(a,b):
    if a < b:
        return a
    return b


def color_box(box, color):
    for _, line_list in box.items():
        for line in line_list:
            line.set_color(color)


def main():
    fontSize=16
    ontime_path = '../processed_data/paper_intermittent_nodes_ontimes680.json'
    offtime_path = '../processed_data/paper_intermittent_nodes_offtimes680.json'
    
    # Data Layout in a file
    ## ['label', [[1,2],[1,3,4,5,],[]...]]
    ## ['label', [[4l,2],[1],[9,3,4]...]]

    # Get the raw data of cis of 8 nodes
    ontime_data = load_cis_data(ontime_path)
    print_debug_info('+++ on-time raw data', ontime_data, getframeinfo(currentframe()).lineno)
    offtime_data = load_cis_data(offtime_path)
    print_debug_info('+++ off-time raw data', offtime_data, getframeinfo(currentframe()).lineno)

    # getting the labels from the data
    ontime_label = get_labels(ontime_data)
    print_debug_info('+++ ontime label', ontime_label, getframeinfo(currentframe()).lineno)
    offtime_label = get_labels(offtime_data)
    print_debug_info('+++ offtime label', ontime_label, getframeinfo(currentframe()).lineno)

    # Get the data without the labels
    unlabelled_ontime_data = get_unlabelled_data(ontime_data)
    print_debug_info('+++ unlabelled ontime data', unlabelled_ontime_data,getframeinfo(currentframe()).lineno )
    unlabelled_offtime_data = get_unlabelled_data(offtime_data)
    print_debug_info('+++ unlabelled offtime data', unlabelled_offtime_data, getframeinfo(currentframe()).lineno)

   ################################################################################ 
    # serialize data
   ################################################################################ 
#    serialized_ontime_data =  serialize_data(unlabelled_ontime_data)
#    print_debug_info('+++ serialized ontime data', serialized_ontime_data, getframeinfo(currentframe()).lineno)
#    serialized_offtime_data =  serialize_data(unlabelled_offtime_data)
#    print_debug_info('+++ serialized offtime data', serialized_offtime_data, getframeinfo(currentframe()).lineno)
#    min_len = 0
#    if len(serialized_ontime_data) < len(serialized_offtime_data):
#        min_len = len(serialized_ontime_data)
#    else:
#        min_len = len(serialized_offtime_data)
#
#
#    ##____ Plotting ____ ##
#    plt.plot(serialized_ontime_data[:min_len], serialized_offtime_data[:min_len], 'x') 
#    plt.show()



    ################################################################################ 

    ################################################################################ 
    cis_experi_nodes_duty_cycle = []
    for cis_idx in range(len(unlabelled_ontime_data)):
        cis=[]
        cis_size = len(unlabelled_ontime_data[cis_idx]) # ideally should be 8
        for node_idx in range(cis_size):
            # get the number of element in the node
            ontime_element_num = len(unlabelled_ontime_data[cis_idx][node_idx])
            offtime_element_num = len(unlabelled_offtime_data[cis_idx][node_idx])
            # use the smallest
            elem_num = __get_the_smaller(ontime_element_num, offtime_element_num)
            node_duty_cycle=[]
            for i in range(elem_num):
               node_duty_cycle.append( unlabelled_ontime_data[cis_idx][node_idx][i]/(\
                       unlabelled_ontime_data[cis_idx][node_idx][i] \
                       + unlabelled_offtime_data[cis_idx][node_idx][i]) * 100) # * 100 for plotting
            cis.append(node_duty_cycle)
        cis_experi_nodes_duty_cycle.append(cis)

    fig = plt.figure(figsize=(8,4))
    color_list = ["#66a61e" , '#e7298a', '#7570b3', '#d95f02', '#1b9e77']
    for idx, cis in enumerate(cis_experi_nodes_duty_cycle):
        box = plt.boxplot(cis, showfliers=False)
        color_box(box,color_list[idx])
    
    plt.gca().grid(True, axis='y') 
    plt.ylabel("Nodes duty cycle (%)", fontsize=fontSize)
    plt.xlabel("Nodes ID", fontsize=fontSize)
    plt.yticks(fontsize=fontSize-2)
    plt.xticks(fontsize=fontSize-2)
    plt.tight_layout()
    plt.savefig('../../paper/figures/natural_light_nodes_duty_cycles.eps')
    plt.show()
    
if __name__=="__main__":
    main()

























