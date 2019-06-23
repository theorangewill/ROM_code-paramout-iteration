#!/bin/bash
if [ $# -gt 0 ]; then
	PAR=cpu
fi
echo $PAR
./install_dep.sh $PAR
sudo singularity exec --nv rom_dnn.sif \
cd code && sh run.sh p
