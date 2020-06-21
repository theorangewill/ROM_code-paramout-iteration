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
	python DNN_regression.py $1 >> $RESULTS_FILE
else
	python DNN_regression.py &&
	python MAE.py &&
	cd .. &&
	cd .. &&
	cd reconst &&
	python reconst_best_model.py 
fi
