#!/bin/bash
if [ $# -gt 0 ]; then
	PAR=cpu
else
	flag=--nv
fi
echo $PAR
./install_dep.sh $PAR
singularity exec $flag ./exec_script.sh 
