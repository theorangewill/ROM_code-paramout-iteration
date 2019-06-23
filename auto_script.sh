#!/bin/bash
sudo apt install -y awscli 
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=AKIATSRODRVJWJ5COHGO
if [ $AWS_SECRET_ACCESS_KEY == '' ]; then
	echo "Insira AWS secret key"
	read akey
	export AWS_SECRET_ACCESS_KEY=$akey
fi
export IID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
git config --global credential.helper 'cache --timeout=86400'
git push
if [ $# -gt 0 ]; then
	PAR=cpu
else
	flag=--nv
fi
echo $PAR
sudo ./install_dep.sh $PAR
sudo singularity exec rom_dnn.sif $flag ./exec_script.sh 
