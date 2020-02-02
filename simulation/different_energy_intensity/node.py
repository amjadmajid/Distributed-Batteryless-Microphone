import numpy as np
class Node:
	def __init__(self, num_pwr_cycles, on_time, off_time):
		self.wake_up_time = np.random.uniform(0,num_pwr_cycles)
		self.on_time  = on_time
		self.off_time = off_time

	def get_wake_up_time(self):
		return self.wake_up_time

	def get_on_time(self):
		return self.on_time

	def get_off_time(self):
		return self.off_time

	def __str__(self):
		return ("Wake up time: "+str(self.wake_up_time)+" on time "+str(self.on_time)+" off_time "+str(self.off_time))

