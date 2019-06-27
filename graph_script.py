#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import numpy as np
import scipy.stats


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    se = scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h

if len(sys.argv) == 1:
    print "Uso: ./graph_script.py <nome arquivo>"

###DICT###
# paramout_vec = [media dos tempos de cada iteracao paramout] (5)
# full_vec      = [media dos tempos de cada iteracao full] (50)
# total_time    = [media do tempo total de 50 iteracoes]   (float)
# total_time_paramout = [media do tempo total de instancias paramout] (float)
# total_time_paramout_vec = [] (float)
# total_time_vec = [vetor com tempos totais de cada 50 iter]
# cost          = [custo on demand de cada instancia]      (float)
# error         = [erro do deviation]                      (float)
##########
res_machines = {'p2.xlarge' : {'cost':0.9},'p3.2xlarge' : {'cost':3.06}, 'c5.2xlarge' : {'cost':0.34}, 'c5.4xlarge' : {'cost':0.68},'c5.9xlarge' : {'cost':1.53}, 'c5.12xlarge' : {'cost':2.04}, 'c5.18xlarge' : {'cost':3.06}, 'c5.24xlarge'  : {'cost':4.08}}

for file in sys.argv[1:]:
    par_cnt = [0.0]*5
    full_cnt = [0.0]*50
    file_name = file[:-4].split('/')[1]
    res_machines[file_name]['total_time'] = 0.0
    res_machines[file_name]['total_time_vec'] = [0.0]*5
    res_machines[file_name]['total_time_paramout'] = 0.0
    res_machines[file_name]['total_time_paramout_vec'] = [0.0]*5
    with open(file,'r') as f:
        ########PARAMOUT########
        f.readline() #paramout
        for i in range(5):
            f.readline() #<n iter>
            f.readline() #COMPUTING DNN REGRESSION
            for j in range(5):
                value = float(f.readline()[:-1].split(':')[1])
                par_cnt[j] = par_cnt[j] + value
                res_machines[file_name]['total_time_paramout'] += value
                res_machines[file_name]['total_time_paramout_vec'][i] += value
            f.readline() #DNN REGRESSION COMPLETE!
        par_cnt = [i/5.0 for i in par_cnt] #media do tempo de cada iteracao
        res_machines[file_name]['total_time_paramout']/= 5.0
        ########FULL########
        f.readline() #full
        for i in range(5):
            f.readline() #<n iter>
            f.readline() #COMPUTING DNN REGRESSION
            for j in range(50):
                value = float(f.readline()[:-1].split(':')[1])
                res_machines[file_name]['total_time'] += value 
                res_machines[file_name]['total_time_vec'][i] += value
                full_cnt[j] = full_cnt[j] + value
            f.readline() #DNN REGRESSION COMPLETE!
        res_machines[file_name]['total_time'] /= 5.0
        full_cnt = [i/5.0 for i in full_cnt]
        #par_cnt.sort()
        #full_cnt.sort()
        res_machines[file_name]['paramout_vec'] = par_cnt
        res_machines[file_name]['full_vec'] = full_cnt
gpu_machines = [i for i in res_machines if i.startswith('p')]
cpu_machines = [i for i in res_machines if i.startswith('c')]

########Computar speedup########
_min = float('inf')
for machine in cpu_machines:
    if res_machines[machine]['total_time'] < _min:
        _min = res_machines[machine]['total_time']
        best_cpu = machine
for machine in cpu_machines:
    res_machines[machine]['speedup'] = res_machines[machine]['total_time']/res_machines[best_cpu]['total_time']
    
_min = float('inf')
for machine in gpu_machines:
    if res_machines[machine]['total_time'] < _min:
        _min = res_machines[machine]['total_time']
        best_gpu = machine
for machine in gpu_machines:
    res_machines[machine]['speedup'] = res_machines[machine]['total_time']/res_machines[best_gpu]['total_time']
print best_cpu, best_gpu 

########Computar speedup para paramount########
_min = float('inf')
for machine in cpu_machines:
    if res_machines[machine]['total_time_paramout'] < _min:
        _min = res_machines[machine]['total_time_paramout']
        best_cpu = machine
for machine in cpu_machines:
    res_machines[machine]['speedup_paramout'] = res_machines[machine]['total_time_paramout']/res_machines[best_cpu]['total_time_paramout']
    
_min = float('inf')
for machine in gpu_machines:
    if res_machines[machine]['total_time_paramout'] < _min:
        _min = res_machines[machine]['total_time_paramout']
        best_gpu = machine
for machine in gpu_machines:
    res_machines[machine]['speedup_paramout'] = res_machines[machine]['total_time_paramout']/res_machines[best_gpu]['total_time_paramout']
print best_cpu, best_gpu 

for machine in res_machines:
    print machine, res_machines[machine]['speedup'], res_machines[machine]['speedup_paramout']
########Computar intervalo de confianca########
for machine in res_machines:
    n = len(res_machines[machine]['total_time_paramout_vec'])
    res_machines[machine]['error'] = mean_confidence_interval(res_machines[machine]['total_time_paramout_vec'])

#for machine in res_machines:
#    print "%s:" %machine
#    print res_machines[machine]
########PARAMOUNT########
x_axis = range(1,6)
plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
for machine in gpu_machines:
    plt.plot(x_axis,res_machines[machine]['paramout_vec'],label=machine)
    plt.legend()
#plt.savefig("paramount-gpu.svg",format="svg")
plt.show()

plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
for machine in cpu_machines:
    plt.plot(x_axis,res_machines[machine]['paramout_vec'],label=machine)
    plt.legend()
#plt.savefig("paramount-cpu.svg",format="svg")
plt.show()

plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
for machine in res_machines:
    plt.plot(x_axis,res_machines[machine]['paramout_vec'],label=machine)
    plt.legend()
#plt.savefig("paramount-all.svg",format="svg")
plt.show()

########FULL########
x_axis = range(1,51)
plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
best_gpu_np = np.array(res_machines[best_gpu]['full_vec'])
for machine in gpu_machines:
    npmachine = np.array(res_machines[machine]['full_vec'])
    plt.plot(x_axis,npmachine/res_machines[machine]['speedup'],label=machine)
    plt.legend()
#plt.savefig("full-norm-gpu.svg",format="svg")
plt.show()

plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
best_cpu_np = np.array(res_machines[best_cpu]['full_vec'])
for machine in cpu_machines:
    npmachine = np.array(res_machines[machine]['full_vec'])
    plt.plot(x_axis,npmachine/res_machines[machine]['speedup'],label=machine)
    plt.legend()
#plt.savefig("full-norm-cpu.svg",format="svg")
plt.show()

plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
for machine in gpu_machines:
    plt.plot(x_axis,res_machines[machine]['full_vec'],label=machine)
    plt.legend()
#plt.savefig("full-cpu.svg",format="svg")
plt.show()

plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
for machine in cpu_machines:
    plt.plot(x_axis,res_machines[machine]['full_vec'],label=machine)
    plt.legend()
#plt.savefig("full-gpu.svg",format="svg")
plt.show()

plt.xlabel('Iteracao')
plt.ylabel('Tempo de execucao [s]')
for machine in res_machines:
    plt.plot(x_axis,res_machines[machine]['full_vec'],label=machine)
    plt.legend()
#plt.savefig("full-all.svg",format="svg")
plt.show()

plt.xlabel('Custo [USD]')
plt.ylabel('Tempo de execucao [s]')
for machine in res_machines:
    full_cost = res_machines[machine]['cost']*res_machines[machine]['total_time_paramout']/3600.0
    full_cost_error = res_machines[machine]['cost']*res_machines[machine]['error']/3600.0
    plt.errorbar(full_cost,res_machines[machine]['total_time_paramout'],res_machines[machine]['error'],full_cost_error,linestyle='None',marker='.',capsize=3,label=machine)
    plt.legend()
plt.savefig("custoxtempo.svg",format="svg")
plt.show()
