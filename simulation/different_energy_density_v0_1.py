import matplotlib.pyplot as plt

e_buf_size = 47000 		# 47000 nF
harv_rate = [8, 30] 	# harvesting rate in shadow and light
e_consump_rate = 120 	# energy consumption rate
nodes_in_shadow = 0.3
num_nodes = 10 			# number of nodes

tot_time = 50000 		# 1000 seconds

# the reason behind this linear relation is the use of voltage regulator 
# that switches between on and off
average_nodes_in_on_time = e_buf_size/e_consump_rate
average_nodes_in_sunlight_off_time = e_buf_size/harv_rate[1]
average_nodes_in_shadow_off_time = e_buf_size/harv_rate[0]


power_cycles_in_sunlight=[]
signal_idx_in_sunlight = 0
signal_value_in_sunlight=[]

for i in range(int(tot_time/(average_nodes_in_on_time+average_nodes_in_sunlight_off_time))):
	signal_idx_in_sunlight += average_nodes_in_on_time
	power_cycles_in_sunlight.append(signal_idx_in_sunlight)
	power_cycles_in_sunlight.append(signal_idx_in_sunlight)
	signal_idx_in_sunlight +=average_nodes_in_sunlight_off_time
	power_cycles_in_sunlight.append(signal_idx_in_sunlight)
	power_cycles_in_sunlight.append(signal_idx_in_sunlight)
	signal_value_in_sunlight.append(1)
	signal_value_in_sunlight.append(0)
	signal_value_in_sunlight.append(0)
	signal_value_in_sunlight.append(1)

power_cycles_in_shadow=[]
signal_idx_in_shadow = 0
signal_value_in_shadow=[]
for i in range(int(tot_time/(average_nodes_in_on_time+average_nodes_in_shadow_off_time))):
	signal_idx_in_shadow += average_nodes_in_on_time
	power_cycles_in_shadow.append(signal_idx_in_shadow)
	power_cycles_in_shadow.append(signal_idx_in_shadow)
	signal_idx_in_shadow +=average_nodes_in_shadow_off_time
	power_cycles_in_shadow.append(signal_idx_in_shadow)
	power_cycles_in_shadow.append(signal_idx_in_shadow)
	signal_value_in_shadow.append(2)
	signal_value_in_shadow.append(1)
	signal_value_in_shadow.append(1)
	signal_value_in_shadow.append(2)

plt.plot(power_cycles_in_sunlight , signal_value_in_sunlight)
plt.plot(power_cycles_in_shadow , signal_value_in_shadow)
plt.show()
