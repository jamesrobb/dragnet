#!/bin/bash

if [ -z "$1" ]; then
	echo "Provide the size of the training set as the first argument"
	exit 1
fi

training_amount=$1
test_amount=`echo "($training_amount * 0.2)/1" | bc`
training_amount=`echo "($training_amount * 0.8)/1" | bc`

head -n $training_amount ./training_set_data/barrays.txt > ./training_set_data/barrays_train.txt
head -n $training_amount ./training_set_data/labels.txt > ./training_set_data/labels_train.txt
tail -n $test_amount ./training_set_data/barrays.txt > ./training_set_data/barrays_test.txt
tail -n $test_amount ./training_set_data/labels.txt > ./training_set_data/labels_test.txt
