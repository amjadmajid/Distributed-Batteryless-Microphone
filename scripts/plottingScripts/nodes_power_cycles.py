from inspect import currentframe, getframeinfo
import numpy as np
import matplotlib.pyplot as plt
import json
plt.style.use('seaborn-ticks')

#-----------------------------------------------------------------
######  #######                     #                             
#     # #           ####  #####     #       #  ####  #    # ##### 
#     # #          #    # #    #    #       # #    # #    #   #   
######  #####      #    # #    #    #       # #      ######   #   
#   #   #          #    # #####     #       # #  ### #    #   #   
#    #  #          #    # #   #     #       # #    # #    #   #   
#     # #           ####  #    #    ####### #  ####  #    #   #   
# ----------------------------------------------------------------
# Run for RF data
rf_flag =True 

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

def boxplot_color_fontsize(box, color, fs):
    for _, line_list in box.items():
        for line in line_list:
            line.set_color(color)
            line.set_linewidth(fs)

def __power_cycle_len(ontime, offtime):
    return ontime + offtime


def main():
    fontSize=20
    if rf_flag:
        ontime_path = '../processed_data/intermittent_nodes_ontimesRF.json'
        offtime_path = '../processed_data/intermittent_nodes_offtimesRF.json'
    else:
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

    # Get the data without the labels
    unlabelled_ontime_data = get_unlabelled_data(ontime_data)[4 if rf_flag else 2]
    print_debug_info('+++ unlabelled ontime data', unlabelled_ontime_data,getframeinfo(currentframe()).lineno )
    unlabelled_offtime_data = get_unlabelled_data(offtime_data)[4 if rf_flag else 2]
    print_debug_info('+++ unlabelled offtime data', unlabelled_offtime_data, getframeinfo(currentframe()).lineno)

    if rf_flag:
        del unlabelled_ontime_data[3]
        del unlabelled_offtime_data[3]

    nodes_indices = range(len(unlabelled_ontime_data))
    nodes_power_cycles_lengths = [[] for i in nodes_indices]
    for node_idx in nodes_indices:
        min_len = __get_the_smaller(len(unlabelled_ontime_data[node_idx]),
                  len(unlabelled_offtime_data[node_idx]))
        for i in range(min_len):
            nodes_power_cycles_lengths[node_idx].append(\
                unlabelled_offtime_data[node_idx][i]+\
                unlabelled_ontime_data[node_idx][i])

    fig = plt.figure(figsize=(8,4))
    color_list = ["#66a61e" , '#e7298a', '#7570b3', '#d95f02', '#1b9e77', '#fc8d59']
    # for idx, cis in enumerate(cis_experi_nodes_duty_cycle[2:3]):
    boxs = plt.boxplot(nodes_power_cycles_lengths, showfliers=False)
    boxplot_color_fontsize(boxs,color_list[1], 1.5)

    
    plt.gca().grid() 
    plt.ylim(bottom=0)
    plt.ylabel("Power cycle (sec)", fontsize=fontSize)
    plt.xlabel("Node ID", fontsize=fontSize)
    plt.yticks(fontsize=fontSize)
    plt.xticks(fontsize=fontSize)
    plt.tight_layout()
    if rf_flag:
        plt.savefig('../../paper_IPSN_2020/figures/rf_power_cycles_len.eps')
    else:
        plt.savefig('../../paper_IPSN_2020/figures/light_power_cycles_len.eps')
    plt.show()
    
if __name__=="__main__":
    main()

























