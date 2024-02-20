tests.py
 1. first part contains the sample provided in question.
 2. Second part has the unit test cases covering all parts of code
 3. used 15 seconds cutoff time instead of 15 minutes to run the test cases quickly.

main.py
 1. Contains classes Trade,CommonStock,PreferredStock,Index which have documented description in help
 2. All the method names are used as given in the question
 3. Addition special methods like __repr__ to print the objects and __add__ to add stocks to Index are used
 4. given an optional price as input to calculate any metric the design will automatically record it as a new price
 5. a positive quantity represents a buy and negative quantity represents a sell

Assumptions:
 1. coded only for market orders. code should be enhanced if limit orders or other types are specified
 2. coded only the parts asked in the question, design should be changed depending on the usecases that will be added.
 3. if the dividend is 0 the P/E ratio is not defined hence None is returned
 4. assumed quantity is not 0 and price greater than 0
 5. stock price is changed when its update function is called or when new price is passed as argument to calculate any metric


