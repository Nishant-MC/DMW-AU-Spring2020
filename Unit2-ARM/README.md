# Association Rule Mining

Lab assignment 2: Association Rule Mining (ARM) using the a priori algorithm.

The assignment code is able to generate random transaction databases to test the implementation upon, and can also compare runtime between the a priori approach and a simple brute force approach.

The assignment code supports 4 runtime configurations:

* **No keyword arguments (kwargs)**: The code will create a database for the sample problem specified in the class slides (4 transactions, some fixed combinations of 4 possible items), as well as a random transaction database according to a few specifications (10-20 transactions, up to 20 unique items, and 1-10 unique items per transaction). The code will then solve the sample problem, first using our implemented a priori approach, as well as a simple brute force approach - the answers should match. After this, it will solve the randomly generated problem using both approaches and displays the results (should also match). It notes the runtime of each approach, so you should be able to compare their performance quite easily.

Example usage from command line:

```
python3 DMW-HW2-vf.py
```

* **2 kwargs**: A local file name and the support threshold S. The code will build a database from the provided sample file (we tested with the ‘Retail’ dataset, retail.txt). The code will then solve the problem using a modified version of our implemented a priori approach meant to work better for this specifically large dataset (16470 unique items, 88162 transactions). It notes the runtime (expect on the order of 6 minutes for the retail dataset for S=10000, lower values of S will take even longer).

Example usage from command line:

```
python3 DMW-HW2-vf.py retail.txt 10000
```

* **4 kwargs**: number of transactions, number of possible unique items, number of unique items per transaction, and the support threshold S for mining association rules from the database. The code will create a random database according to the specifications, print it, and then solve the problem using our implemented a priori approach. It will also measure runtime of the algorithm. Example usage from the command line (1000 transactions, 20 possible items, 10 items per transaction, S=100):

```
python3 DMW-HW2-vf.py 1000 20 10 100
```

(*Caution*: Runtime can be high for large databases [10000+ transactions] with many items per transaction. Start with small kwargs and then ramp up)


* **5 kwargs**: number of transactions, number of possible unique items, lower & upper bounds for the number of unique items per transaction, and the support threshold S for mining association rules from the database. The code will create a random database according to the specifications, print it, and then solve the problem using our implemented a priori approach. It will also measure runtime of the algorithm. Example usage from the command line (1000 transactions, 20 possible items, 1-10 items per transaction, S=50):

```
python3 DMW-HW2-vf.py 1000 20 1 10 50
```

**The code is self-documenting and should explain reasonably well what each function is doing and why. Reference the code comments when needed.**

**CAUTION: There is no input validation for the supplied runtime arguments, because implementing that is a waste of time for the purposes of this assignment. So don’t mess around with invalid inputs or impossible configurations, they will at best make the code crash and at worst lead to unpredictable behavior.**


Example full runs:

```
nishantcoding$ python3 DMW-HW2-vf.py 20 10 1 5 3
Five kwargs specified:
# transactions, # possibles, # uniques / transaction LB & UB, support threshold (S)...

Random DB ( 20 transactions, 10 possible items, 1 to 5 items per transaction):
(1, {'D', 'C', 'E', 'A'})
(2, {'I', 'H', 'C'})
(3, {'E'})
(4, {'D', 'C', 'A'})
(5, {'I', 'D', 'B'})
(6, {'H', 'A'})
(7, {'C', 'F', 'I', 'E', 'G'})
(8, {'A'})
(9, {'I', 'D', 'J', 'F'})
(10, {'D', 'C', 'I', 'J', 'H'})
(11, {'D', 'B'})
(12, {'A', 'I', 'F', 'E', 'H'})
(13, {'I', 'A', 'E', 'F'})
(14, {'C', 'F'})
(15, {'I', 'C', 'J', 'B'})
(16, {'I', 'H', 'B', 'E'})
(17, {'H', 'J', 'B', 'F'})
(18, {'C', 'A', 'J', 'E', 'B'})
(19, {'H', 'G', 'F', 'B'})
(20, {'H', 'F'})

Test problem (ARM) solution ( S = 3 ): [('A', 7), ('B', 7), ('C', 8), ('D', 6), ('E', 7), ('F', 8), ('H', 8), ('I', 9), ('J', 5), ('AC', 3), ('AE', 4), ('BH', 3), ('BI', 3), ('BJ', 3), ('CD', 3), ('CE', 3), ('CI', 4), ('CJ', 3), ('DI', 3), ('EF', 3), ('EI', 4), ('FH', 4), ('FI', 4), ('HI', 4), ('IJ', 3), ('EFI', 3)]
Time taken (seconds): 0.0018360614776611328
```

```
nishantcoding$ python3 DMW-HW2-vf.py retail.txt 10000
Reading the transaction database provided in retail.txt ...
Support threshold S specified: 10000

File DB:
(1, {'13', '17', '4', '19', '22', '8', '9', '0', '2', '28', '1', '27', '10', '23', '25', '5', '11', '20', '16', '15', '18', '29', '3', '12', '14', '26', '6', '24', '7', '21'})
…
(88161, {'2528', '39', '48'})
(88162, {'39', '32', '242', '205', '1393'})
The file is being parsed into a transaction db. It has...
16470 unique items in 88162 transactions.
Finding candidate singletons above the specified threshold...
1000 candidates processed.
2000 candidates processed.
3000 candidates processed.
4000 candidates processed.
5000 candidates processed.
6000 candidates processed.
7000 candidates processed.
8000 candidates processed.
9000 candidates processed.
10000 candidates processed.
11000 candidates processed.
12000 candidates processed.
13000 candidates processed.
14000 candidates processed.
15000 candidates processed.
16000 candidates processed.
Candidate singleton items have been found.
Singletons are: [({'48'}, 42135), ({'32'}, 15167), ({'41'}, 14945), ({'39'}, 50675), ({'38'}, 15596)]
Performing a priori association rule mining...
Task completed.

File problem (ARM) solution ( S = 10000 ): [({'48'}, 42135), ({'32'}, 15167), ({'41'}, 14945), ({'39'}, 50675), ({'38'}, 15596), ({'39', '48'}, 29142), ({'39', '41'}, 11414), ({'39', '38'}, 10345)]
Time taken (seconds): 346.5947208404541
```