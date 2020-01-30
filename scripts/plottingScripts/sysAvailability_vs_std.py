from inspect import currentframe, getframeinfo
import numpy as np
import matplotlib.pyplot as plt
import json
plt.style.use('seaborn-ticks')

light_avail = [27.2817402684564  ,50.55366508474577 ,67.57647099999996 ,80.0495618729097  ,91.34881903171953]
light_std   = [42.89184473358219, 47.66594845913576, 44.29264143185064, 37.79610571696741, 24.985479669137185]

rf_avail = [61.05714432291658 ,55.51594662863079 ,43.22395614583315 ,33.54103734375005 ,21.50304765625002]
rf_std = [8.803991947784114 ,8.829239998874275 ,7.388289069824066 ,8.454807364202034 ,7.128776523566454]

rf_std = rf_std[::-1]
rf_avail = rf_avail[::-1]

plt.plot(light_avail, light_std)
plt.plot(rf_avail, rf_std)

fontSize = 18

plt.gca().grid(True, axis='y') 
plt.ylabel("std", fontsize=fontSize)
plt.xlabel("Availability", fontsize=fontSize)
# plt.xticks(np.arange(5)+1,(300,500,800,1000,1400),fontsize=fontSize-2)
plt.yticks(fontsize=fontSize-2)
plt.xticks(fontsize=fontSize-2)
plt.tight_layout()
plt.savefig('../../paper/figures/sysAvailability_vs_std.eps')
plt.show()
    
if __name__=="__main__":
    main()