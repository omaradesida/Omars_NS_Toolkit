import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from scipy.signal import find_peaks, peak_widths

import os
import re


rootdir = "/PWD/"
regex = re.compile('(analyse.dat)')


anal_list = []


#exclude = ["64_atoms"]

for root, dirs, files in os.walk(rootdir):
  dirs[:] = [d for d in dirs if d not in exclude]
  for file in files:
    if regex.match(file):
       anal_list.append(root+"/"+file)




fig,ax = plt.subplots()
ax.set_xlim(0,5)
#ax.set_xlim(-0.5,32)
ax.set_ylabel(r"Pressure, $p\sigma^3/\epsilon$")
ax.set_xlabel(r"Temperature, $k_{B}T/ \epsilon$")
ax.set_yscale("log")
ax.set_title(r"Phase Diagram for $r_c = 1.2$")


pressures = []
temp_peaks = []
peak_hw = []

print("#Pressure Temp HalfWidthMaximum")

for i in anal_list:
    try:
        p_txt = re.search("P([0-9]*[.])?[0-9]+\/",i)
        pressure = float(p_txt.group()[1:-1])

        data = np.loadtxt(i)
    
        try:
            heat_capacity = data[:,4]
            temps = data[:,0]
        except:
            continue

        heat_capacity_peaks,_ = find_peaks(heat_capacity, height = 200)


        ipeak_hw = peak_widths(heat_capacity,heat_capacity_peaks)[0]
        ipeak_hw = ipeak_hw*(temps[1]-temps[0]) + temps[0]
        peak_hw = np.concatenate([peak_hw,ipeak_hw])


        for i in heat_capacity_peaks:
            pressures.append(pressure)
            temp_peaks.append(temps[i])
            print(pressure,temps[i], ipeak_hw[0])
    except:
        continue
        


    
plt.errorbar(temp_peaks,pressures,xerr = peak_hw,marker = ".", ls = "None", capsize = 3.0, mew=0.5, elinewidth=0.5, c = "k")

plt.show()
#lt.savefig("phase_diagram.ps")
