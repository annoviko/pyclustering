
import numpy
import random
import math




def clustering( numberOfAnts, size_lattice, maxIteration, clusteringData, count_data ):
    random.seed()

    alpha = 3;
    gamaPick = 0.1;
    gamaDrop = 0.3;
    #dropProbability = 0.5;

    #directionProbability = 0.5;
    neighborSize = 1;

    #stepSize = 1;
    directionStep = [ [-1, -1], [0, -1], [1, -1], [-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0] ];

    lattice = numpy.zeros( (size_lattice + neighborSize, size_lattice + neighborSize) ); # +neighborSize for excluding control outstep under bound
    bDataOnLattice = numpy.zeros( (count_data ) );
    dataOnLattice = numpy.zeros( (count_data, 2) );
    neighborsData = numpy.zeros( (count_data) );
    pickupPAnt = numpy.zeros( (maxIteration, numberOfAnts) );

    lambda_py = numpy.zeros( (maxIteration, numberOfAnts) );
    dropPAnt = numpy.zeros( (maxIteration, numberOfAnts) );

    ant_data = numpy.zeros( (count_data) )
    ant_location = numpy.zeros( (size_lattice*size_lattice) )

    for i in range(count_data):
        ant_data[i]  = i;
    random.shuffle( ant_data );

    for i in range(size_lattice * size_lattice):
        ant_location[i]  = i;
    random.shuffle( ant_location );

    ants_direct     = numpy.zeros( (numberOfAnts) )
    ants_location1  = numpy.zeros( (numberOfAnts) )
    ants_location2  = numpy.zeros( (numberOfAnts) )
    ants_datum      = numpy.zeros( (numberOfAnts) )

    #-------------- calc Distance Matrix ----------------------
    distanceMatrix = numpy.zeros( (count_data, count_data) );
    for i in range(count_data):
        for j in range( i+1,count_data ):
            distanceMatrix[i][j] = math.sqrt( (clusteringData[i][0] - clusteringData[j][0])**2 + (clusteringData[i][0] - clusteringData[j][0])**2 )
            distanceMatrix[j][i] =  distanceMatrix[i][j];

    #-------------- end calc Distance Matrix ------------------

    for dataNum in range( count_data ):
        dataOnLattice[dataNum][0] = math.ceil( ant_location[dataNum] / size_lattice );
        dataOnLattice[dataNum][1] =  math.ceil( ant_location[dataNum] % size_lattice + 1);
        lattice[ dataOnLattice[dataNum][0], dataOnLattice[dataNum][1] ] = dataNum;
        bDataOnLattice[ dataNum ] = 1;

    for antNum in range( numberOfAnts ):
        ants_direct[ antNum ] = random.randrange(8);

        #set data to ant from random permutation array
        ants_datum[ antNum ] = ant_data[ antNum ];
        #get data from lattice to ant
        ants_location1[ antNum ] = dataOnLattice[ ants_datum[ antNum ], 0 ];
        ants_location2[ antNum ] = dataOnLattice[ ants_datum[ antNum ], 1 ];

        lattice[ ants_location1[ antNum ], ants_location2[ antNum ] ] = 0;
        bDataOnLattice[ ants_datum[ antNum ] ] = 0;


    for iterNumber in range( maxIteration ):
        #disp( iterNumber );
        #disp( lattice );
        # cycle for antNum or random select
        for antNum in range( numberOfAnts ):
            # set step direction for ants
            # TODO
            doStep = 0;
            while ( doStep == 0 ):
                randNumber = random.randrange(8);

                if( ants_location1[antNum] + directionStep[randNumber][0] > 0 and ants_location1[antNum] + directionStep[randNumber][0] < size_lattice ):
                    if( ants_location2[antNum] + directionStep[randNumber][1] > 0 and ants_location2[antNum] + directionStep[randNumber][1] < size_lattice ):
                        ants_location1[antNum] = ants_location1[antNum] + directionStep[randNumber][0];
                        ants_location2[antNum] = ants_location2[antNum] + directionStep[randNumber][1];
                        doStep = 1;

            # TODO set random direction to agent
            # check border

            # if cell filled
            if( lattice[ants_location1[antNum], ants_location2[antNum]] != 0 ):
                continue;

            # find neighbors
            # neighborsAnts[] -- length numOfNeighbors
            count_neigh = 0;
            for x in range( -neighborSize, neighborSize + 1 ):
                for y in range( -neighborSize , neighborSize + 1 ):
                    if( ants_location1[antNum]+x >= 0 and ants_location2[antNum]+y >= 0 ):
                        if( lattice[ ants_location1[antNum]+x, ants_location2[antNum]+y ] != 0 ):
                            count_neigh = count_neigh + 1;
                            neighborsData[ count_neigh ] = lattice[ ants_location1[antNum]+x, ants_location2[antNum]+y ];

            if( count_neigh > 0 ):
                # calc distance between curAnt and all their neighbors
                # d === dist_neighbor
                d = numpy.zeros( count_neigh );
                for neighAntIt in range( count_neigh ):
                    d[neighAntIt] = distanceMatrix[ ants_datum[antNum] ][ neighborsData[neighAntIt] ];


                # calc f(i)
                summ = 0.0;
                for i in range( count_neigh ):
                    summ += 1 - d[i] / alpha

                lambda_py[iterNumber, antNum] = max( 0, (1/count_neigh**2)*summ );
                llamb = lambda_py[iterNumber][antNum];


                #Drop stage
                dropPAnt[iterNumber] [antNum] = ( lambda_py[iterNumber, antNum] / ( gamaDrop + lambda_py[iterNumber][antNum] ))**2;
                pPAnt = dropPAnt[iterNumber][antNum];
            else:
                dropPAnt[iterNumber] [antNum] = 0;
                pPAnt = dropPAnt[iterNumber][antNum];

            randNumber = random.random();

            #
            if (dropPAnt[iterNumber][antNum] > randNumber) :
                #drop data
                lattice[ ants_location1[ antNum ], ants_location2[ antNum ] ] = ants_datum[ antNum ];
                #bDataOnLattice( ants_datum[ antNum ] ) = 1;

                dataOnLattice[ ants_datum[ antNum ], 0 ] = ants_location1[ antNum ];
                dataOnLattice[ ants_datum[ antNum ], 1 ] = ants_location2[ antNum ];

                pick = 0;
                while ( pick == 0 ):
                    # Random select datum
                    rndData = random.randrange(count_data);
                    if( bDataOnLattice[rndData] == 0 ):
                        continue;
                    # neighborsAnts[] -- length numOfNeighbors
                    count_neigh = 0;
                    for x in range ( -neighborSize, neighborSize ):
                        for y in range ( -neighborSize, neighborSize ):
                            if( x != 0 and y != 0 and dataOnLattice[rndData][0]+x > 0 and dataOnLattice[rndData][1]+y > 0 ):
                                if( lattice[ dataOnLattice[ rndData][0]+x, dataOnLattice[rndData][1]+y ] != 0 ):
                                    count_neigh = count_neigh + 1;
                                    neighborsData[ count_neigh ] = lattice[ dataOnLattice[rndData][0]+x, dataOnLattice[rndData][1]+y ];

                    # calc distance between curAnt and all their neighbors
                    # d === dist_neighbor
                    if( count_neigh > 0 ):
                        d = numpy.zeros( count_neigh );
                        for neighAntIt in range( count_neigh ):
                            d[neighAntIt] = distanceMatrix[ ants_datum[antNum] , neighborsData[neighAntIt] ];


                        # calc f(i)
                        summ = 0.0;
                        for i in range( count_neigh ):
                            summ += 1 - d[i] / alpha
                        lambda_py_pick = max( 0, (1/count_neigh**2) * summ );

                        #Pick up stage
                        pickupPAnt[iterNumber][antNum] = (gamaPick / (gamaPick + lambda_py_pick) )**2;
                        ppick = pickupPAnt[iterNumber][antNum];
                    else:
                        pickupPAnt[iterNumber][antNum] = 1;
                        ppick = pickupPAnt[iterNumber][antNum];

                    randNumber = random.random();
                    # TODO

                    if( pickupPAnt[iterNumber][antNum] > randNumber ):
                        pick = 1;
                        bDataOnLattice[ ants_datum[ antNum ] ] = 1;

                        ants_datum[ antNum ] = rndData;
                        ants_location1[ antNum ] = dataOnLattice[ ants_datum[ antNum ], 0 ];
                        ants_location2[ antNum ] = dataOnLattice[ ants_datum[ antNum ], 1 ];

                        lattice[ ants_location1[ antNum ], ants_location2[ antNum ] ] = 0;
                        bDataOnLattice[ ants_datum[ antNum ] ] = 0;


    #---- end for iterNumber

    for antNum in range( numberOfAnts ):
        lattice[  dataOnLattice[ ants_datum[ antNum ], 0 ], dataOnLattice[ants_datum[ antNum ], 1 ] ] = ants_datum[ antNum ];
        bDataOnLattice[ ants_datum[ antNum ] ] = 1;

    return lattice


# file = open("../sample.txt", 'r');
#
# sample = [[float(val) for val in line.split()] for line in file];
#
# file.close();
#
# print( clustering( 10, 11, 100000, sample, 42 ) )

