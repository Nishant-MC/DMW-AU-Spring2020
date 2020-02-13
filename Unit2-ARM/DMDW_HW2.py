"""
# Data Mining & Warehousing, Spring 2020
# Group Assignment: Gopal S, Mihret MA, Nishant MC
"""


# Necessary imports to make the assignment much less tedious
import sys
from time import time
from copy import deepcopy
from random import randint

# Only used for the brute force comparison, not in the actual AP algorithm
from itertools import combinations


# Quick function to create the test database mentioned in the slides
def generate_testdb():
    return [ ( 1, { 'A', 'B', 'C'} ) ,
             ( 2, { 'A', 'C'} ) ,
             ( 3, { 'A', 'D', 'E' } ) ,
             ( 4, { 'B', 'C' } ) ]


"""
# Function which generates a random database of LBn-UBn transactions
# Each transaction has some combination of k (b/w LBt & UBt) possible items 
# NO DUPLICATE ITEMS ALLOWED IN A TRANSACTION
"""
def generate_randomdb(LBn, UBn, k, LBt, UBt):
    database = []
    
    for i in range( randint(LBn,UBn) ):
        items = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                  'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ][0:k]
        basket = set()
        
        for j in range( randint(LBt,UBt) ):
            basket.add( items.pop( randint( 0, len(items)-1 ) ) )

        database.append( (i+1, basket) )
        
    return database


"""
# Some quick printer / returner functions for coding convenience / readability
"""
# Function which prints a given transaction database (no return value)
def print_db(database):
    for item in database:
        print(item)

# Function which prints a given combination object (no return value)
def print_combination(combo):
    for i in list(combo):
        print(i)

# Quick function to return the item set only from the (item set, frequency) 2-tuple
def return_candidates(candidates):
    return [ item[0] for item in candidates ]


"""
# Some handy sorting keys for displaying results
# Keys are: length of itemlist, dictionary order of itemlist string, itemlist support #
"""
def key_listlength(a):
    return len(a[0])

def key_dictorder(a):
    return ''.join(list(a[0]))

def key_support(a):
    return a[1]


"""
# Finding new candidates by (1) iterating through a candidate list and then
# (2) checking each potential candidate against a transaction db
# All viable candidates must be above support threshold S
"""
def find_new_candidates(database, possiblecandidates, support):

    candidates = []
    
    # Perform a linear pass (search) for each candidate over the full transaction db
    for item in possiblecandidates:
        s = 0
        # Check if the candidate itemset is a subset of the current transaction's itemset
        for transaction in database:
            if set(item).issubset(transaction[1]):
                s += 1
        # Only add the candidate itemset to your list if it crosses the support threshold
        if s >= support:
            candidates.append( (''.join( sorted( list( item ) ) ), s) )
            
    return candidates


"""
# Function to find new candidate strings of length i given two other pieces of info:
# (1) A list of viable candidates above support threshold S [up to length i-1]
# (2) A list of viable singletons (length 1 strs) above support threshold S
# The output is a list of potential candidates of length i
"""
def find_new_combinations( kncandidates, singletons, i ):

    ilist = []
    
    # For every candidate in kncandidates...
    for candidate in kncandidates:
        # If its length is i-1...
        if len(candidate[0]) == i-1:
            # For every viable singleton....
            for s in singletons:
                # Join together the i-1 string and the singleton. Sorted order
                temp = ''.join( sorted( list( s[0] + candidate[0] ) ) )
                # If this join remains length i and isn't in the ilist, add it
                if ( temp not in ilist ) and ( len(set(temp)) == len(temp) ):
                    ilist.append(temp)

    return ilist


"""
# Function which implements brute force association rule mining on a database
# Parameter support is the minimum support threshold S
"""
def brute_arm(database, support):

    # First find the set of all possible items
    possibleitems = set()
    for transaction in database:
        possibleitems = possibleitems.union( transaction[1] )

    # Next, populate the list of candidates with sets of 1 above threshold S
    kncandidates = find_new_candidates(database, possibleitems, support)
    
    # Keep a copy of just these viable singletons for later computations
    singletons = deepcopy(kncandidates)

    """
    # Now repeat the process iteratively using nCi combinations of the viable singletons
    # NOTE: This is a quick hack with VERY slow runtime over large datasets
            A better solution uses each iterated list of length i sets to get new candidates
    """
    for i in range(2, len(kncandidates)+1):
        newcombinations = list( combinations( return_candidates( singletons ) ,i ) )
        kncandidates.extend( find_new_candidates(database, newcombinations, support) )

    # Return the result, sorted by: list length, and then by dictionary order of itemlist
    return sorted( sorted(kncandidates,key=key_dictorder),key=key_listlength )

    
"""
# Function which implements a priori association rule mining on a database
# Parameter support is the minimum support threshold S
"""
def apriori_arm(database, support):

    # First find the set of all possible items
    possibleitems = set()
    for transaction in database:
        possibleitems = possibleitems.union( transaction[1] )

    # Next, populate the list of candidates with sets of 1 above threshold S
    kncandidates = find_new_candidates(database, possibleitems, support)
    
    # Keep a copy of just these viable singletons for later iterations
    singletons = deepcopy(kncandidates)

    # Now repeat iteratively using combinations of singletons and found candidates
    for i in range(2, len(kncandidates)+1):
        newcombinations = find_new_combinations ( kncandidates, singletons, i )
        kncandidates.extend( find_new_candidates(database, newcombinations, support) )

    # Return the result, sorted by: list length, and then by dictionary order of itemlist
    return sorted( sorted(kncandidates,key=key_dictorder),key=key_listlength )



# Main function
def main():

    # Default behavior
    if len(sys.argv) == 1:
        
        print('No keyword args supplied - resorting to default behavior...')
    
        # Generating the test case
        transactiondb = generate_testdb()
        print('\nTest DB:')
        print_db(transactiondb)

        # Generating a random case
        randomdb = generate_randomdb(10,20,15,1,10)
        print('\nRandom DB (10-20 transactions, 15 possible items, 1-10 items per transaction):')
        print_db(randomdb)

        # Solving the test case (association rule mining)
        candidatesets = apriori_arm(transactiondb, 2)
        print('\nTest problem (ARM) solution (S=2):', candidatesets)

        # Solving the test case (brute force)
        candidatesets = brute_arm(transactiondb, 2)
        print('\nTest problem (brute) solution (S=2):', candidatesets)

        # Solving the randomly generated case (association rule mining)
        start = time()
        candidatesets = apriori_arm(randomdb, 3)
        end = time()
        print('\nTest problem (ARM) solution (S=3):', candidatesets)
        print('Time taken (seconds):', end-start)

        # Solving the randomly generated case (brute force)
        start = time()
        candidatesets = brute_arm(randomdb, 3)
        end = time()
        print('\nRandom problem (brute) solution (S=3):', candidatesets)
        print('Time taken (seconds):', end-start)

    # If 4 kwargs (# transactions, # possible items, # uniques / transaction, support thresh S) are given 
    elif len(sys.argv) == 5:

        print('Four kwargs specified:')
        print('# transactions, # possible items, # unique items / transaction, support threshold (S)...')

        randomdb = generate_randomdb( int(sys.argv[1]), int(sys.argv[1]), int(sys.argv[2]),
                                      int(sys.argv[3]), int(sys.argv[3]) )
        print('\nRandom DB (', sys.argv[1], 'transactions,', sys.argv[2], 'possible items,',
              sys.argv[3], 'items per transaction):' )
        
        print_db(randomdb)

        # Solving the randomly generated case (association rule mining)
        start = time()
        candidatesets = apriori_arm(randomdb, int(sys.argv[4]) )
        end = time()
        print('\nTest problem (ARM) solution (S:', sys.argv[4], '):', candidatesets)
        print('Time taken (seconds):', end-start)

    # If 5 kwargs (# transactions, # possible items, # uniques / transact LB + UB, supp thresh) are given 
    elif len(sys.argv) == 6:

        print('Five kwargs specified:')
        print('# transactions, # possibles, # uniques / transaction LB & UB, support threshold (S)...')

        randomdb = generate_randomdb( int(sys.argv[1]), int(sys.argv[1]), int(sys.argv[2]),
                                      int(sys.argv[3]), int(sys.argv[4]) )
        print('\nRandom DB (', sys.argv[1], 'transactions,', sys.argv[2], 'possible items,',
              sys.argv[3], 'to', sys.argv[4], 'items per transaction):' )
        
        print_db(randomdb)

        # Solving the randomly generated case (association rule mining)
        start = time()
        candidatesets = apriori_arm(randomdb, int(sys.argv[5]) )
        end = time()
        print('\nTest problem (ARM) solution ( S =', sys.argv[5], '):', candidatesets)
        print('Time taken (seconds):', end-start)

    # Handling undefined input cases
    else:
        print('ERROR: Unrecognized combination of keyword arguments.')
    

if __name__ == "__main__":
    main()
