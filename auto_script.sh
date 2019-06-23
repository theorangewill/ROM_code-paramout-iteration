#!/bin/bash
if [ $# -gt 0 ]; then
	PAR=cpu
fi
echo $PAR
./install_dep.sh $PAR
singularity exec --nv rom_dnn.sif \
cd code && sh run.sh p
