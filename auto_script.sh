#!/bin/bash
if [ $# -gt 0 ]; then
	PAR=cpu
else
	flag=--nv
fi
echo $PAR
./install_dep.sh $PAR
singularity exec rom_dnn.sif $flag ./exec_script.sh 
