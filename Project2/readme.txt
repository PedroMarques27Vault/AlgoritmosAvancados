Approximate Counting With Fixed Probability Counter and Csurös Counter
-To execute the code, simply run:
	python3 counter.py d prob_in_fraction trials
		example: python3 counter 5 1/32 1000
	It Will read all text files inside the 'text' folder
All results are in csv files inside the results folder, with the correct language identified (En,Fr,Ne,Ge)
	The 'Exact' files represent the exact counter values

	The 'FixedProbability' files represent the fixed probability counter values over 1000 trials for prob=1/32

	The 'CsurosCounter' files represent the csuros counter values over 1000 trials for d = 8

The statistics files present calculated statistics
	-The second line is the mean counter values 
		->For the csuros counter, each entry is a tuple (counter, t,u)

	The third line presents the min,max, mad and standard deviation
	The 4th line represents the min, max and avg estimated counter value error (i.e the comparison between obtained counter value and estimated)
	The 5th line represents the min, max and avg estimated real value error (i.e the comparison between the calculated real value using the counter's data and the real value from the exact counter)


Work done by Pedro Marques
92926