# Association Rule Mining

Lab assignment 2: Association Rule Mining (ARM) using the a priori algorithm.

The assignment code is able to generate random transaction databases to test the implementation upon, and can also compare runtime between the a priori approach and a simple brute force approach.

The assignment code supports 3 runtime configurations:

* **No keyword arguments (kwargs)**: The code will create a database for the sample problem specified in the class slides (4 transactions, some fixed combinations of 4 possible items), as well as a random transaction database according to a few specifications (10-20 transactions, up to 20 unique items, and 1-10 unique items per transaction). The code will then solve the sample problem, first using our implemented a priori approach, as well as a simple brute force approach - the answers should match. After this, it will solve the randomly generated problem using both approaches and displays the results (should also match). It notes the runtime of each approach, so you should be able to compare their performance quite easily.

Example usage from command line:

```
python3 DMW-HW2-vf.py
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


Example full run:

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