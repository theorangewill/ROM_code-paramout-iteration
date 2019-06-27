#!/bin/bash
cd ..
RESULTS_FILE=$(pwd)/results.txt
cd code/
cp inputs.inp pod/ &&
cd pod/ &&
sh clean.sh &&
sh compileOpt.sh &&
./pod && 
cd .. &&
cd regression/compact_scheme/ &&
sh compile.sh &&
./calc_derivative.out &&
cd .. &&
cd deep_learning/
if [ "$#" -gt 0 ]; then
	PARAMOUT=$1
	FULL=$2
	rm $RESULTS_FILE
	echo "paramout" >> $RESULTS_FILE 
	for i in `seq 1 5`
	do
		echo $i >> $RESULTS_FILE
		python DNN_regression.py $PARAMOUT >> $RESULTS_FILE
	done
	echo "full" >> $RESULTS_FILE
	for i in `seq 1 5`
	do
		echo $i >> $RESULTS_FILE
		python DNN_regression.py $FULL >> $RESULTS_FILE
	done
else
	python DNN_regression.py &&
	python MAE.py &&
	cd .. &&
	cd .. &&
	cd reconst &&
	python reconst_best_model.py 
fi
