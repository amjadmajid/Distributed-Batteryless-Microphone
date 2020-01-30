from inspect import currentframe, getframeinfo
import numpy as np
import matplotlib.pyplot as plt
import json
plt.style.use('seaborn-ticks')

# To disable debugging set it to False
# To print all debugging info set the second entry to 0
# To print a specific message set its id
DEBUG = [False, 0]

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

def cleaned_data(data):
    cleaned_cis=[]
    for cis in data:
        cleaned_cis.append(np.array(cis[0]) * 100 )  # * 100 for plotting 
    return cleaned_cis

def get_labels(data):
    return __get_column(data,0)

def get_unlabelled_data(data):
    return __get_column(data,1)

def __get_column(data,idx):
    col=[]
    for row in data:
        col.append(row[idx])
    return col


def color_box(box, color):
    for _, line_list in box.items():
        for line in line_list:
            line.set_color(color)


def main():
    fontSize=16
    ontime_path = '../processed_data/new/availabilityTimeline470_sleep_interval5.json'
    
    # Data Layout in a file
    ## ['label', [[1,2],[1,3,4,5,],[]...]]
    ## ['label', [[4l,2],[1],[9,3,4]...]]

    # Get the raw data of cis of 8 nodes
    ontime_data = load_cis_data(ontime_path)
    print_debug_info('+++ on-time raw data', ontime_data, getframeinfo(currentframe()).lineno)
 
    # getting the labels from the data
    ontime_label = get_labels(ontime_data)
    print_debug_info('+++ ontime label', ontime_label, getframeinfo(currentframe()).lineno)

    # Get the data without the labels
    unlabelled_ontime_data = get_unlabelled_data(ontime_data)
    print_debug_info('+++ unlabeled ontime data', unlabelled_ontime_data,getframeinfo(currentframe()).lineno )

    clean_data = cleaned_data(unlabelled_ontime_data)
    # print (clean_data, file=open("debug.txt", 'w'))
    # exit()
    fig = plt.figure(figsize=(8,4))

    # for idx, cis in enumerate(clean_data):
    colors = ["#d73027", "#fee090", "#4575b4"]
    label = [ '900 lux', '500 lux','800 lux']
    patterns=['-+', '-o', '->', '-x', '-s', '-*']
    for i in range(len(clean_data)):
        # print(np.mean(clean_data[i]),"&", np.std(clean_data[i]))
        plt.plot(clean_data[i], patterns[i], label=label[i], color=colors[i])
    # box = plt.boxplot(clean_data, showfliers=False)
    # color_box(box, "#000000")
    
    plt.gca().grid(True, axis='y') 
    plt.ylabel("Availability (%)", fontsize=fontSize)
    plt.xlabel("Seconds", fontsize=fontSize)
    # plt.xticks(np.arange(5)+1,(300,500,800,1000,1400),fontsize=fontSize-2)
    plt.yticks(fontsize=fontSize-2)
    plt.xticks(fontsize=fontSize-2)
    plt.legend(fontsize=fontSize, loc="lower right")
    plt.tight_layout()
    plt.savefig('../../paper/figures/sysAvailabilityTimeline_470_sleep_5seconds.eps')
    plt.show()
    
if __name__=="__main__":
    main()