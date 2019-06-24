#!/usr/bin/python

import matplotlib.pyplot as plt
import sys

if len(sys.argv) == 1:
    print "Uso: ./graph_script.py <nome arquivo>"

res_machines = {}
for file in sys.argv[1:]:
    par_cnt = [0.0]*5
    full_cnt = [0.0]*50
    file_name = file[:-4]
    with open(file,'r') as f:
        ########PARAMOUT########
        f.readline() #paramout
        for i in range(5):
            f.readline() #<n iter>
            f.readline() #COMPUTING DNN REGRESSION
            for j in range(5):
                value = float(f.readline()[:-1].split(':')[1])
                par_cnt[j] = value
            f.readline() #DNN REGRESSION COMPLETE!
        par_cnt = [i for i in par_cnt] #media do tempo de cada iteracao
    ########FULL########
        f.readline() #full
        for i in range(5):
            f.readline() #<n iter>
            f.readline() #COMPUTING DNN REGRESSION
            for j in range(50):
                value = float(f.readline()[:-1].split(':')[1])
                full_cnt[j] = value
            f.readline() #DNN REGRESSION COMPLETE!
        full_cnt = [i for i in full_cnt]
        par_cnt.sort()
        full_cnt.sort()
        res_machines[file_name] = [par_cnt,full_cnt]
x_axis = range(1,51)
for machine in res_machines:
    plt.plot(x_axis,res_machines[machine][1],label=machine)
    plt.legend()
plt.show()
