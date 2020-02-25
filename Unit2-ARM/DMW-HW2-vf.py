"""
# Data Mining & Warehousing, Spring 2020
# Group Assignment: Gopal S, Mihret MA, Nishant MC
# Assignment 2 (Lab): ASSOCIATION RULE MINING

Github repo link for more info (all labs + writeups):
https://github.com/Nishant-MC/DMW-AU-Spring2020
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
# Function which generates a database from a given input file
# It assumes each line is a space-delimited set of items bought together
# It goes line by line through the file, strips the trailing newline and splits by space
# It uses this preprocessed input to build up the database (i = transaction id)
"""
def parse_filedb(file):
    database = []
    i = 0

    for line in open(file):
        i += 1
        database.append( (i, set(line.strip('\n').split(' ')[:-1]) ) )

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

# Quick function to return the item set only from a (item set, frequency) 2-tuple
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
# Finding new candidates by:
# (1) iterating through a candidate list and then
# (2) checking each potential candidate against a transaction db
# All viable candidates must be above support threshold S
"""
def find_new_candidates(database, possiblecandidates, support):

    candidates = []

    # Perform a linear pass (search) for each candidate over the full transaction db
    for itemset in possiblecandidates:
        s = 0
        # Check if the candidate itemset is a subset of the current transaction's itemset
        for transaction in database:
            if set(itemset).issubset(transaction[1]):
                s += 1
        # Only add the candidate itemset to your list if it crosses the support threshold
        if s >= support:
            candidates.append( (''.join( sorted( list( itemset ) ) ), s) )
            
    return candidates

"""
# Same candidate finding function, adapted for the retail.txt dataset 
"""
def find_new_candidates_adapted(database, possiblecandidates, support):

    candidates = []

    i = 0
    # Perform a linear pass (search) for each candidate over the full transaction db
    for itemset in possiblecandidates:
        i += 1
        if (i % 1000) == 0:
            print(i, 'candidates processed.')
        s = 0
        # Check if the candidate itemset is a subset of the current transaction's itemset
        for transaction in database:
            if itemset.issubset(transaction[1]):
                s += 1
        # Only add the candidate itemset to your list if it crosses the supp threshold
        if s >= support:
            candidates.append( ( itemset, s ) )
            
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
                # If this join is length i and isn't in the ilist, add it
                if ( temp not in ilist ) and ( len(set(temp)) == len(temp) ):
                    ilist.append(temp)

    return ilist

"""
# Same combination finding function, adapted for the retail.txt dataset 
"""
def find_new_combinations_adapted( kncandidates, singletons, i ):

    ilist = []
    
    # For every candidate in kncandidates...
    for candidate in kncandidates:
        # If its length is i-1...
        if len(candidate[0]) == i-1:
            # For every viable singleton....
            for s in singletons:
                # Join together the i-1 string and the singleton
                temp = s[0].union(candidate[0])
                # If this join is length i and isn't in the ilist, add it
                if ( temp not in ilist ) and ( len(temp) != len(candidate[0]) ):
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
    for i in range(2, len(singletons)+1):
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
    
    """
    # Now repeat iteratively using appropriate combinations of singletons and found candidates
    # The function find_new_combinations() is used for implementation of the a priori algorithm
    # We use it to iteratively build and prune candidate lists level by level as needed
    # Max number of possible levels = number of unique items in the viable singleton set
    """
    for i in range(2, len(singletons)+1):
        newcombinations = find_new_combinations( kncandidates, singletons, i )
        kncandidates.extend( find_new_candidates(database, newcombinations, support) )

    # Return the result, sorted by: list length, and then by dictionary order of itemlist
    return sorted( sorted(kncandidates,key=key_dictorder),key=key_listlength )


def make_singleton_set(item):
    result = set()
    result.add(item)
    return result

"""
# Apriori ARM function, adapted for the retail.txt dataset 
"""
def apriori_adapted(database, support):

    # First find the set of all possible items
    possibleitems = set()
    print('The file is being parsed into a transaction db. It has...')
    
    for transaction in database:
        possibleitems = possibleitems.union( transaction[1] )
    print(len(possibleitems), 'unique items in', len(database), 'transactions.')

    possibleitems = [ make_singleton_set(item) for item in list(possibleitems) ]

    # Next, populate the list of candidates with sets of 1 above threshold S
    print('Finding candidate singletons above the specified threshold...')
    kncandidates = find_new_candidates_adapted(database, possibleitems, support)
    print('Candidate singleton items have been found.')
    
    # Keep a copy of just these viable singletons for later iterations
    singletons = deepcopy(kncandidates)
    print('Singletons are:', singletons)
    
    """
    # Now repeat iteratively using appropriate combinations of singletons and found candidates
    # The function find_new_combinations() is used for implementation of the a priori algorithm
    # We use it to iteratively build and prune candidate lists level by level as needed
    # Max number of possible levels = number of unique items in the viable singleton set
    """
    print('Performing a priori association rule mining...')
    for i in range(2, len(singletons)+1):
        newcombinations = find_new_combinations_adapted( kncandidates, singletons, i )
        kncandidates.extend( find_new_candidates_adapted(database, newcombinations, support) )

    print('Task completed.')
    # Return the result, sorted by: list length, and then by dictionary order of itemlist
    return sorted( kncandidates, key=key_listlength )



# Main function (where everything happens)
def main():

    # Default behavior if no keyword arguments (kwargs) are supplied...
    if len(sys.argv) == 1:
        
        print('No keyword arguments supplied - resorting to default behavior...')
    
        # Generating the test case
        transactiondb = generate_testdb()
        print('\nTest DB:')
        print_db(transactiondb)

        # Generating a random case
        randomdb = generate_randomdb(10,20,20,1,10)
        print('\nRandom DB (10-20 transactions, 20 possible items, 1-10 items per transaction):')
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

    # Default behavior if a file name to read from is supplied...
    elif len(sys.argv) == 3:

        print('Reading the transaction database provided in', sys.argv[1], '...')
        print('Support threshold S specified:', sys.argv[2])
        transactiondb = parse_filedb(sys.argv[1])
        print('\nFile DB:')
        print_db(transactiondb)

        start = time()
        candidatesets = apriori_adapted( transactiondb, int(sys.argv[2]) )
        end = time()
        print('\nFile problem (ARM) solution ( S =', int(sys.argv[2]) , '):', candidatesets)
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
        print('\nTest problem (ARM) solution ( S =', sys.argv[4], '):', candidatesets)
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
    


# Calling the main function from the global namespace
if __name__ == "__main__":
    main()
