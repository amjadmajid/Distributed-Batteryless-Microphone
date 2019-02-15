import csv

def read_csv_file(file): 
    output_list=[]
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        line = csv_reader.next()
        if 'Time' not in line[0]:
            output_list.append(line)

        for line in csv_reader:
            output_list.append(line)
        return output_list

print( read_csv_file('../data/DIS_uptime/850_lux.csv'))
