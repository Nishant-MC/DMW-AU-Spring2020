import sys
from random import uniform, randint

def create_dataset( cmin, cmax, dimensions, ptsLB, ptsUB , output ):

    numberofpoints = randint(ptsLB,ptsUB)
    print('\nOutput file:', output)
    print('Dimensionsality of data points:', dimensions)
    print('Number of data points created:', numberofpoints)
    print('Min and max values for coordinates:', cmin, '-', cmax)

    data = [ tuple( [ uniform(cmin,cmax) for i in range(dimensions) ] )
             for i in range( numberofpoints ) ]

    opfile = open(output,'w')

    for coordinates in data:
        for i in range( len(coordinates) ):
            opfile.write( str(coordinates[i]) )
            if i != len(coordinates)-1:
                opfile.write(' ')
        opfile.write('\n')

    opfile.close()


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print('No kwargs given: default behavior engaged...')
        print('Creating a database of between 10k-20k points in 2-d.')
        print('Each point (x,y) is a float tuple b/w (0,0) and (1000,1000).')
        create_dataset( 0, 1000, 2, 10000, 20000, 'output.txt' )
        
    elif len(sys.argv) == 6:
        print('Kwargs given: cmin, cmax, dimensionality, number of pts, opfile')
        create_dataset( float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]),
                        int(sys.argv[4]), int(sys.argv[4]), sys.argv[5] )

    elif len(sys.argv) == 7:
        print('Kwargs given: cmin, cmax, dimensionality, #pts LB, #pts UB, opfile')
        create_dataset( float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]),
                        int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] )

    else:
        print('Unrecognized configuration. Required kwarg count: 0, 5 or 6')
        print('Acceptable kwargs: cmin, cmax, dimensionality, #pts LB, #pts UB, opfile')
