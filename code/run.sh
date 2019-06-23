#!/bin/bash
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
        echo "Redirecionando saida para paramout_dnn.txt"
        rm paramout_dnn.txt
	for i in {1..5}
	do
		echo i >> paramout_dnn.txt
		python DNN_regression.py $1 >> paramout_dnn.txt 
	done
	else
		python DNN_regression.py &&
                python MAE.py &&
                cd .. &&
                cd .. &&
                cd reconst &&
                python reconst_best_model.py 
fi







