# Necessary imports to make the assignment much less tedious
from copy import deepcopy
from random import randint
from itertools import combinations

# Quick function to create the test database mentioned in the slides
def generate_testdb():
    return [ ( 1, { 'A', 'B', 'C'} ) ,
             ( 2, { 'A', 'C'} ) ,
             ( 3, { 'A', 'D', 'E' } ) ,
             ( 4, { 'B', 'C' } ) ]

"""
# Function which generates a random database of 5-10 transactions
# Each transaction has some combination of 8 possible items (1-5 items each)
"""
def generate_randomdb():
    database = []
    
    for i in range( randint(5,10) ):
        items = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
        basket = set()
        
        for j in range( randint(1,5) ):
            basket.add( items.pop( randint( 0, len(items)-1 ) ) )

        database.append( (i+1, basket) )
        
    return database

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
# Finding new candidates from a candidate list in a transaction db
# Candidates ust be above support threshold S
"""
def find_new_candidates(database, possiblecandidates, support):
    candidates = []
    for item in possiblecandidates:
        s = 0
        for transaction in database:
            if set(item).issubset(transaction[1]):
                s += 1
        if s >= support:
            candidates.append( (item, s) )
    return candidates


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
    # Now repeat the process iteratively using nCi combinations of the viable singletons
    # NOTE: This is a quick hack with slow runtime over large datasets
            A better solution uses each iterated list of length i sets to get new candidates
    """
    for i in range(2, len(kncandidates)+1):
        newcombinations = list( combinations( return_candidates( singletons ) ,i ) )
        kncandidates.extend( find_new_candidates(database, newcombinations, support) )

    return kncandidates
    


# Main function
def main():
    
    # Generating the test case
    transactiondb = generate_testdb()
    print('\nTest DB:')
    print_db(transactiondb)

    # Generating a random case
    randomdb = generate_randomdb()
    print('\nRandom DB:')
    print_db(randomdb)

    # Solving the test case
    candidatesets = apriori_arm(transactiondb, 2)
    print('\nTest problem solution (S=2):', candidatesets)

    # Solving the randomly generated case
    candidatesets = apriori_arm(randomdb, 3)
    print('\nRandom problem solution (S=3):', candidatesets)


if __name__ == "__main__":
    main()
