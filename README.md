# Decision-Tree-using-ID3

Language : Python

Packages required to run the program :
------------------------------------
	pandas - used to extract data from csv file
	math   - used for logarithmic function
	random - used to get a random number between 0 & 1 when no instances are there at a node
	sys    - used to pass variables from the command prompt

How to run the program :
----------------------
python ID3.py /filepath/training_data_set /filepath/validation_data_set /filepath/testing_data_set pruning_factor

for instance -
--------------
for data set 1
--------------
python ID3.py  C:/Users/kgasw/Grad/data_sets1/training_set.csv C:/Users/kgasw/Grad/data_sets1/validation_set.csv C:/Users/kgasw/Grad/data_sets1/test_set.csv 0.2
--------------
for data set 2
--------------
python ID3.py  C:/Users/kgasw/Grad/data_sets2/training_set.csv C:/Users/kgasw/Grad/data_sets2/validation_set.csv C:/Users/kgasw/Grad/data_sets2/test_set.csv 0.2
