#!/usr/bin/python

import matplotlib.pyplot as plt
import sys

if len(sys.argv) == 1:
    print "Uso: ./graph_script.py <nome arquivo>"

###DICT###
# paramount_vec = [media dos tempos de cada iteracao paramout] (5)
# full_vec      = [media dos tempos de cada iteracao full] (50)
# total_time    = [media do tempo total de 50 iteracoes]   (float)
# cost          = [custo on demand de cada instancia]      (float)
##########
res_machines = {p2.xlarge = {cost:0.9},p3.2xlarge = {cost:3.06}, c5.2xlarge = {cost:0.34}, c5.4xlarge = {cost:0.68},c5.9xlarge = {cost:1.53}, c5.12xlarge = {cost:2.04}, c5.18xlarge = {cost:3.06}, c5.24xlarge  = {cost:4.08}}

for file in sys.argv[1:]:
    par_cnt = [0.0]*5
    full_cnt = [0.0]*50
    file_name = file[:-4].split('/')[1]
    with open(file,'r') as f:
        ########PARAMOUT########
        f.readline() #paramout
        for i in range(5):
            f.readline() #<n iter>
            f.readline() #COMPUTING DNN REGRESSION
            for j in range(5):
                value = float(f.readline()[:-1].split(':')[1])
                par_cnt[j] = par_cnt[j]+ value
            f.readline() #DNN REGRESSION COMPLETE!
        par_cnt = [i/5.0 for i in par_cnt] #media do tempo de cada iteracao
        ########FULL########
        f.readline() #full
        for i in range(5):
            f.readline() #<n iter>
            f.readline() #COMPUTING DNN REGRESSION
            for j in range(50):
                value = float(f.readline()[:-1].split(':')[1])
                full_cnt[j] = full_cnt[j] + value
            f.readline() #DNN REGRESSION COMPLETE!
        full_cnt = [i/5.0 for i in full_cnt]
        #par_cnt.sort()
        #full_cnt.sort()
        res_machines[file_name][paramount_vec]=par_cnt
        full_cnt

x_axis = range(1,6)
for machine in res_machines:
    plt.plot(x_axis,res_machines[machine][0],label=machine)
    plt.legend()
plt.show()
