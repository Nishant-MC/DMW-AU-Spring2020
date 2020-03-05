import sys
import numpy as np
from copy import deepcopy
from random import choice

"""
# Reads an input file to create an array of n-dimensional coordinates
# Input: A .txt file where each line is a space-delimited set of coordinates
# Output: np.array of float vectors (works for arbitrary dimensionality of n)
"""
def read_dataset( ipfile ):
    return np.array( [ np.float_( line.rstrip().split(' ') )
                       for line in open(ipfile, 'r') ] )

"""
# Performs k-means clustering on an array of n-dimensional coordinates
# Inputs: the array of n-d coordinates, # of clusters (k), # of max iterations (execlimit)
# Output: array of ints indicating cluster group for each set of coordinates
"""
def kmeans_clustering( coordDB, k, execlimit ):
    
    # Initializing array for result processing
    result = np.zeros( len(coordDB) )
    
    # Randomly choosing k initial cluster centers + making a copy of the choices
    centroids = np.array( [ choice( coordDB ) for i in range(k) ] )
    prevcentroids = deepcopy(centroids)

    # Initializing a distance matrix + execution counter
    distances = np.zeros( (len(coordDB), k) )
    execcount = 0

    # K-means clustering master loop
    while True:
        
        # Incrementing loop execution counter
        execcount += 1
        print('K-means clustering loop', execcount, '- computing new centroids...')
        
        # For every point in the coordinate database
        for i in range( len(coordDB) ):
            
            # For every centroid in the list of centroids
            for j in range( len(centroids) ):
                
                # Calculate the L2 norm of the point and the centroid and store it
                # NOTE: The L2 norm b/w two points is simply its Euclidean distance
                distances[i][j] = np.linalg.norm( coordDB[i]-centroids[j], ord=2 )

            # Do a correct cluster assignment for the point
            # NOTE: The assignment is randomly chosen if 2 or more centroids are equidistant
            result[i] = choice( np.where( distances[i] == np.amin(distances[i]) )[0] )

        # Recompute cluster centroids 
        centroids = recompute_centroids( coordDB, k, result )

        # Break conditions: checking for centroid convergence + if limit of max iterations reached
        # NOTE: Update prevcentroids and go again if no break conditions are met
        if np.array_equal( centroids, prevcentroids ):
            print('\nThe K-means algorithm has converged.')
            break
        elif execlimit == execcount:
            print('\nExecution limit reached. Breaking out...')
            break
        else:
            prevcentroids = deepcopy(centroids)

    
    # Return the computed cluster assignments
    return result


# Computing cluster centroids by averaging the coordinate values of each cluster
def recompute_centroids( coordDB, k, clusteringresult ):
    newcentroids = np.zeros( ( k, len(coordDB[0]) ) )
    divisors = np.zeros( k )
    
    for i in range( len(clusteringresult) ):
        newcentroids[ int(clusteringresult[i]) ] += coordDB[i]
        divisors[ int(clusteringresult[i]) ] += 1

    for j in range( len(newcentroids) ):
        newcentroids[j] /= divisors[j]

    print(newcentroids)
    return newcentroids


# Helper function to do a quick count of many points each cluster has
def analyze_clusters( kmeansresult ):
    (unique, count) = np.unique( kmeansresult, return_counts=True )
    frequencies = np.asarray( (unique,count) ).T
    for f in frequencies:
        print('Cluster', int(f[0]+1), 'contains', int(f[1]), 'elements.')


# Plotter function for mapping out the results of k-means clustering (not yet implemented)
def plot_clusters( coordDB, kmeansresult ):
    pass


# Main function wrapper
def main():
    if len(sys.argv) == 4:
        print('Three kwargs given: input file, number of clusters (k), k-means iteration limit')

        coordDB = read_dataset( sys.argv[1] )
        print('Initial dataset:\n', coordDB, '\n')
        print('Total number of points:', len(coordDB))
        print('Dimensionality of points:', len(coordDB[0]), '\n')
        
        kmeansresult = kmeans_clustering( coordDB, int(sys.argv[2]), int(sys.argv[3]) )
        analyze_clusters( kmeansresult )
        plot_clusters( coordDB, kmeansresult )


if __name__ == "__main__":
    main()
