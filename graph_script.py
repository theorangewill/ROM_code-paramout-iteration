# coding: utf-8
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
res_machines = {'_p2.xlarge' : {'cost':0.9},'_p3.2xlarge' : {'cost':3.06}, '_c5.2xlarge' : {'cost':0.34}, '_c5.4xlarge' : {'cost':0.68},'_c5.9xlarge' : {'cost':1.53}, '_c5.12xlarge' : {'cost':2.04}, '_c5.18xlarge' : {'cost':3.06}, '_c5.24xlarge'  : {'cost':4.08},'_g3s.xlarge' : {'cost':0.75}}
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'darkviolet', 'lawngreen', 'darkturquoise', 'deeppink', 'teal', 'gold', 'salmon', 'saddlebrown']

#for file in sys.argv[1:]:
#    par_cnt = [0.0]*5
#    full_cnt = [0.0]*50
#    file_name = file[:-4].split('/')[1]
#    res_machines[file_name]['total_time'] = 0.0
#    #res_machines[file_name]['total_time_vec'] = [0.0]*5
#    res_machines[file_name]['total_time_paramout'] = 0.0
#    #res_machines[file_name]['total_time_paramout_vec'] = [0.0]*5
#    with open(file,'r') as f:
#        ########PARAMOUT########
#        f.readline() #paramout
#        #for i in range(5):
#        f.readline() #<n iter>
#        f.readline() #COMPUTING DNN REGRESSION
#        for j in range(5):
#            value = float(f.readline()[:-1].split(':')[1])
#            par_cnt[j] = par_cnt[j] + value
#            res_machines[file_name]['total_time_paramout'] += value
#            #res_machines[file_name]['total_time_paramout_vec'] += value
#        f.readline() #DNN REGRESSION COMPLETE!
#        #par_cnt = [i/5.0 for i in par_cnt] #media do tempo de cada iteracao
#        res_machines[file_name]['total_time_paramout']
#        ########FULL########
#        f.readline() #full
#        #for i in range(5):
#        f.readline() #<n iter>
#        f.readline() #COMPUTING DNN REGRESSION
#        for j in range(50):
#            value = float(f.readline()[:-1].split(':')[1])
#            res_machines[file_name]['total_time'] += value 
#            #res_machines[file_name]['total_time_vec'] += value
#            full_cnt[j] = full_cnt[j] + value
#        f.readline() #DNN REGRESSION COMPLETE!
#        res_machines[file_name]['total_time']
#        full_cnt = [i/5.0 for i in full_cnt]
#        #par_cnt.sort()
#        #full_cnt.sort()
#        res_machines[file_name]['paramout_vec'] = par_cnt
#        res_machines[file_name]['full_vec'] = full_cnt


for file in sys.argv[1:]:
    par_cnt = [0.0]*5
    full_cnt = [0.0]*50
    file_name = file[:-4].split('/')[1]
    res_machines[file_name]['total_time'] = 0.0
    res_machines[file_name]['total_time_paramout'] = 0.0
    res_machines[file_name]['total_time_1'] = 0.0
    res_machines[file_name]['total_time_10'] = 0.0
    
    with open(file,'r') as f:
        ########PARAMOUT########
        f.readline() #paramout
        f.readline() #<n iter>
        f.readline() #COMPUTING DNN REGRESSION
        for j in range(5):
            value = float(f.readline()[:-1].split(':')[1])
            par_cnt[j] = value
            res_machines[file_name]['total_time_paramout'] += value
            if j == 0:
                res_machines[file_name]['total_time_1'] += value
        f.readline() #DNN REGRESSION COMPLETE!
        ########FULL########
        f.readline() #full
        #for i in range(5):
        f.readline() #<n iter>
        f.readline() #COMPUTING DNN REGRESSION
        for j in range(50):
            value = float(f.readline()[:-1].split(':')[1])
            res_machines[file_name]['total_time'] += value 
            if j < 10:
                res_machines[file_name]['total_time_10'] += value
            full_cnt[j] = value
        f.readline() #DNN REGRESSION COMPLETE!
        #par_cnt.sort()
        #full_cnt.sort()
        res_machines[file_name]['paramout_vec'] = par_cnt
        res_machines[file_name]['full_vec'] = full_cnt
        res_machines[file_name]['avg_paramount'] = res_machines[file_name]['total_time_paramout']/5.0
        res_machines[file_name]['avg_full'] = res_machines[file_name]['total_time']/50.0



gpu_machines = [i for i in res_machines if i.startswith('_p') or i.startswith('_g')]
cpu_machines = [i for i in res_machines if i.startswith('_c')]

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


########Computar speedup para 1########
_min = float('inf')
for machine in cpu_machines:
    if res_machines[machine]['total_time_1'] < _min:
        _min = res_machines[machine]['total_time_1']
        best_cpu = machine
for machine in cpu_machines:
    res_machines[machine]['speedup_1'] = res_machines[machine]['total_time_1']/res_machines[best_cpu]['total_time_1']
    
_min = float('inf')
for machine in gpu_machines:
    if res_machines[machine]['total_time_1'] < _min:
        _min = res_machines[machine]['total_time_1']
        best_gpu = machine
for machine in gpu_machines:
    res_machines[machine]['speedup_1'] = res_machines[machine]['total_time_1']/res_machines[best_gpu]['total_time_1']
print best_cpu, best_gpu 

print res_machines['_p2.xlarge']

########Computar speedup para 10########
_min = float('inf')
for machine in cpu_machines:
    if res_machines[machine]['total_time_10'] < _min:
        _min = res_machines[machine]['total_time_10']
        best_cpu = machine
for machine in cpu_machines:
    res_machines[machine]['speedup_10'] = res_machines[machine]['total_time_10']/res_machines[best_cpu]['total_time_10']
    
_min = float('inf')
for machine in gpu_machines:
    if res_machines[machine]['total_time_10'] < _min:
        _min = res_machines[machine]['total_time_10']
        best_gpu = machine
for machine in gpu_machines:
    res_machines[machine]['speedup_10'] = res_machines[machine]['total_time_10']/res_machines[best_gpu]['total_time_10']
print best_cpu, best_gpu 


for machine in res_machines:
    print machine, res_machines[machine]['speedup_1'], res_machines[machine]['speedup_paramout'], res_machines[machine]['speedup_10'], res_machines[machine]['speedup']
########Computar intervalo de confianca########
#for machine in res_machines:
#    n = len(res_machines[machine]['total_time_paramout_vec'])
#    res_machines[machine]['error'] = mean_confidence_interval(res_machines[machine]['total_time_paramout_vec'])

#for machine in res_machines:
#    print "%s:" %machine
#    print res_machines[machine]
########PARAMOUNT########
plt.rcParams.update({'font.size': 13})
plt.ylim(15,60)
x_axis = range(1,6)
plt.xlabel(u"Iteração")
plt.ylabel(u'Tempo de execução [s]')
for machine,clr in zip(gpu_machines,colors):
    plt.plot(x_axis,res_machines[machine]['paramout_vec'],label=machine[1:])
    plt.xticks(x_axis)
    plt.legend()
plt.savefig("graficos/paramount-gpu.svg",format="svg",color=clr)
plt.show()

plt.ylim(15,60)
plt.xlabel(u'Iteração')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr in zip(cpu_machines,colors):
    plt.plot(x_axis,res_machines[machine]['paramout_vec'],label=machine[1:])
    plt.xticks(x_axis)
    plt.legend()
plt.savefig("graficos/paramount-cpu.svg",format="svg",color=clr)
plt.show()

plt.ylim(15,60)
plt.xlabel(u'Iteração')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr in zip(res_machines,colors):
    plt.plot(x_axis,res_machines[machine]['paramout_vec'],label=machine[1:])
    plt.xticks(x_axis)
    plt.legend()
plt.savefig("graficos/paramount-all.svg",format="svg",color=clr)
plt.show()

########FULL########
x_axis = range(1,51)
#plt.xlabel('Iteracao')
#plt.ylabel('Tempo de execucao [s]')
#best_gpu_np = np.array(res_machines[best_gpu]['full_vec'])
#for machine in gpu_machines:
#    npmachine = np.array(res_machines[machine]['full_vec'])
#    plt.plot(x_axis,npmachine/res_machines[machine]['speedup'],label=machine[1:])
#    plt.legend()
##plt.savefig("graficos/full-norm-gpu.svg",format="svg")
#plt.show()
#
#plt.xlabel('Iteracao')
#plt.ylabel('Tempo de execucao [s]')
#best_cpu_np = np.array(res_machines[best_cpu]['full_vec'])
#for machine in cpu_machines:
#    npmachine = np.array(res_machines[machine]['full_vec'])
#    plt.plot(x_axis,npmachine/res_machines[machine]['speedup'],label=machine[1:])
#    plt.legend()
##plt.savefig("graficos/full-norm-cpu.svg",format="svg")
#plt.show()

plt.ylim(15,60)
plt.xlabel(u'Iteração')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr in zip(gpu_machines,colors):
    plt.plot(x_axis,res_machines[machine]['full_vec'],label=machine[1:])
    plt.legend()
plt.savefig("graficos/full-cpu.svg",format="svg",color=clr)
plt.show()

plt.ylim(15,60)
plt.xlabel(u'Iteração')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr in zip(cpu_machines,colors):
    plt.plot(x_axis,res_machines[machine]['full_vec'],label=machine[1:])
    plt.legend()
plt.savefig("graficos/full-gpu.svg",format="svg",color=clr)
plt.show()

plt.figure(num=None, figsize=(10, 9), dpi=80, facecolor='w', edgecolor='k')
plt.ylim(15,60)
plt.xlabel(u'Iteração')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr in zip(res_machines,colors):
    plt.plot(x_axis,res_machines[machine]['full_vec'],label=machine[1:])
    #plt.legend()
plt.legend(loc='upper right', ncol=4)
plt.savefig("graficos/full-all.svg",format="svg",color=clr)
plt.show()
markes = ['o','v','^','<','>','s','*','X','D','1','P']

plt.xlabel('Custo [USD]')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr,mark in zip(res_machines,colors,markes):
    full_cost = res_machines[machine]['cost']*res_machines[machine]['total_time_paramout']/3600.0
    #full_cost_error = res_machines[machine]['cost']*res_machines[machine]['error']/3600.0
    plt.scatter(full_cost,res_machines[machine]['total_time_paramout'],linestyle='None',marker=mark,label=machine[1:],color=clr,s = 80)

    plt.legend()
plt.savefig("graficos/custoxtempo-par.svg",format="svg")
plt.show()


plt.xlabel('Custo [USD]')
plt.ylabel(u'Tempo de execução [s]')
for machine,clr,mark in zip(res_machines,colors,markes):
    full_cost = res_machines[machine]['cost']*res_machines[machine]['total_time']/3600.0
    #full_cost_error = res_machines[machine]['cost']*res_machines[machine]['error']/3600.0
    plt.scatter(full_cost,res_machines[machine]['total_time'],linestyle='None',marker=mark,label=machine[1:],color=clr,s = 80)

    plt.legend()
plt.savefig("graficos/custoxtempo-full.svg",format="svg")
plt.show()

for machine in res_machines:
    res_machines[machine]['total_cost_1'] = res_machines[machine]['total_time_1']*res_machines[machine]['cost']/3600.0
    res_machines[machine]['total_cost_paramount'] = res_machines[machine]['total_time_paramout']*res_machines[machine]['cost']/3600.0
    res_machines[machine]['total_cost_10'] = res_machines[machine]['total_time_10']*res_machines[machine]['cost']/3600.0
    res_machines[machine]['total_cost_full'] = res_machines[machine]['total_time']*res_machines[machine]['cost']/3600.0

min_cost = [float('inf')]*4
cost_overhead_min = ['']*4
string_usage = ['total_cost_1','total_cost_paramount','total_cost_10','total_cost_full']
for machine in res_machines:
    for i in range(4):
        if res_machines[machine][string_usage[i]] < min_cost[i]:
            min_cost[i] = res_machines[machine][string_usage[i]]
            cost_overhead_min[i] = machine

print '\n',min_cost
print cost_overhead_min
print "################################ OVERHEAD COST ################################"
for machine in res_machines:
    res_machines[machine]['overhead_cost_1'] = res_machines[machine]['total_cost_1']/res_machines[cost_overhead_min[0]]['total_cost_1']
    res_machines[machine]['overhead_cost_paramount'] = res_machines[machine]['total_cost_paramount']/res_machines[cost_overhead_min[1]]['total_cost_paramount']
    res_machines[machine]['overhead_cost_10'] = res_machines[machine]['total_cost_10']/res_machines[cost_overhead_min[2]]['total_cost_10']
    res_machines[machine]['overhead_cost_full'] = res_machines[machine]['total_cost_full']/res_machines[cost_overhead_min[3]]['total_cost_full']

for machine in res_machines:
    print machine,res_machines[machine]['overhead_cost_1'],res_machines[machine]['overhead_cost_paramount'],res_machines[machine]['overhead_cost_10'],res_machines[machine]['overhead_cost_full'] 
machine_names = [i[1:] for i in res_machines]
avg_times_par = [i['avg_paramount'] for i in res_machines.values()]
avg_times_full = [i['avg_full'] for i in res_machines.values()]
width = 0.35
ind = np.arange(len(avg_times_full))

fig,ax = plt.subplots()
rects1 = ax.bar(ind - width/2, avg_times_par,width,label='Media de tempos Paramount')
rects2 = ax.bar(ind + width/2, avg_times_full,width,label='Media de tempos da Execucao Total')
ax.set_ylabel('Tempo (s)');
ax.set_title('Tempo por grupo (paramount ou execucao total)')
ax.set_xticks(ind)
ax.set_xticklabels(machine_names)
ax.legend()
fig.tight_layout()
plt.show()
