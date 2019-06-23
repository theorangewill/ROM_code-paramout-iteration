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
	PARAMOUT=5
	FULL=50
	ITYPE=$(curl http://169.254.169.254/latest/meta-data/instance-type).txt
        rm $ITYPE
	echo "paramout" >> $ITYPE 
	for i in `seq 1 5`
	do
		echo $i >> $ITYPE
		python DNN_regression.py $PARAMOUT >> $ITYPE
	done
	echo "full" >> $ITYPE
	for i in `seq 1 5`
	do
		echo $i >> $ITYPE
		python DNN_regression.py $FULL >> $ITYPE
	done
	mv $ITYPE ../../../results/.
	cd ../../..
	git add results/$ITYPE
	git commit -m "$ITYPE"
	git push && aws ec2 terminate-instances --instance-ids $IID
	else
		python DNN_regression.py &&
                python MAE.py &&
                cd .. &&
                cd .. &&
                cd reconst &&
                python reconst_best_model.py 
fi







