function [ lattice, dataOnLattice, bDataOnLattice, ants, latticeFirst ] = clustering( numberOfAnts, size_lattice, maxIteration, clusteringData )

    count_data = length( clusteringData );

    alpha = 10;
    gamaPick = 0.1;
    gamaDrop = 0.3;
    %dropProbability = 0.5;
    
    %directionProbability = 0.5;
    neighborSize = 2;
    
    stepSize = 1;
    directionStep = stepSize * [-1 -1; 0 -1; 1 -1; -1 1; 0 1; 1 1; -1 0; 1 0];
    
    lattice = zeros( size_lattice + neighborSize ); % +neighborSize for exluding control outstep under bound
    bDataOnLattice = zeros( 1, length( clusteringData ) );
    dataOnLattice = zeros( count_data, 2 );
    neighborsData = zeros( count_data, 1 );
    pickupPAnt = zeros( maxIteration, numberOfAnts );
    
    lambda = zeros( maxIteration, numberOfAnts );
    dropPAnt = zeros( maxIteration, numberOfAnts );
    
    ant_data = randperm(count_data);
    ant_location = randperm( size_lattice * size_lattice );
    
    ants( numberOfAnts ).direction = 0;
    ants( numberOfAnts ).location(1) = 0;
    ants( numberOfAnts ).location(2) = 0;
    ants( numberOfAnts ).datum = 0;
    
    %-------------- calc Distance Matrix ----------------------
    distanceMatrix = zeros( count_data );
    for i = 1:count_data
        for j = i+1:count_data
            distanceMatrix(i,j) = sqrt( (clusteringData(i,1) - clusteringData(j,1))^2 + (clusteringData(i,2) - clusteringData(j,2))^2 );
            distanceMatrix(j,i) =  distanceMatrix(i,j);
        end
    end
    %-------------- end calc Distance Matrix ------------------
    
    for dataNum = 1:count_data
        dataOnLattice( dataNum, 1 ) = ceil( ant_location(dataNum) / size_lattice );
        dataOnLattice( dataNum, 2 ) =  ceil(mod( ant_location(dataNum), size_lattice ) + 1);
        lattice( dataOnLattice( dataNum, 1 ), dataOnLattice( dataNum, 2 ) ) = dataNum;
        bDataOnLattice( dataNum ) = 1;
    end
    
    latticeFirst = lattice;
    
    for antNum = 1:numberOfAnts
        ants( antNum ).direction = randi(8);

        %set data to ant from random permutation array
        ants( antNum ).datum = ant_data( antNum );
        %get data from lattice to ant
        ants( antNum ).location(1) = dataOnLattice( ants( antNum ).datum, 1 );
        ants( antNum ).location(2) = dataOnLattice( ants( antNum ).datum, 2 );
        
        lattice( ants( antNum ).location(1), ants( antNum ).location(2) ) = 0;
        bDataOnLattice( ants( antNum ).datum ) = 0;        
    end

    for iterNumber = 1:maxIteration
        %disp( iterNumber );
        %disp( lattice );
        % cycle for antNum or random select
        for antNum = 1:numberOfAnts
            % set step direction for ants
            % TODO
            doStep = 0;
            while ~doStep
                randNumber = randi(8);
            
                if( ants(antNum).location(1) + directionStep(randNumber,1) > 0 && ants(antNum).location(1) + directionStep(randNumber,1) <= size_lattice )
                    if ants(antNum).location(2) + directionStep(randNumber,2) > 0 && ants(antNum).location(2) + directionStep(randNumber,2) <= size_lattice
                        ants(antNum).location(1) = ants(antNum).location(1) + directionStep(randNumber,1);
                        ants(antNum).location(2) = ants(antNum).location(2) + directionStep(randNumber,2);
                        doStep = 1;
                    end
                end
            % TODO set random direction to agent
            % check border    
            end
            
            % if cell filled
            if( lattice(ants(antNum).location(1), ants(antNum).location(2)) ~= 0 ) 
                continue;
            end
            
            % find neighbors
            % neighborsAnts[] -- length numOfNeighbors
            count_neigh = 0;
            for x = -neighborSize : neighborSize
                for y = -neighborSize : neighborSize
                    if( ants(antNum).location(1)+x > 0 && ants(antNum).location(2)+y > 0 )
                        if( lattice( ants(antNum).location(1)+x, ants(antNum).location(2)+y ) ~= 0 )
                            count_neigh = count_neigh + 1;
                            neighborsData( count_neigh ) = lattice( ants(antNum).location(1)+x, ants(antNum).location(2)+y );
                        end
                    end
                end 
            end
            
            % calc distance between curAnt and all their neighbors
            % d === dist_neighbor
            d = zeros( count_neigh, 1 );
            for neighAntIt = 1:count_neigh
                d(neighAntIt) = distanceMatrix( ants(antNum).datum , neighborsData(neighAntIt) );
            end
 
            % calc f(i)
            lambda(iterNumber, antNum) = max( 0, (1/count_neigh^2)*sum(1 - d./alpha) );
            llamb = lambda(iterNumber, antNum);
            %Drop stage
            dropPAnt(iterNumber, antNum) = ( lambda(iterNumber, antNum) / ( gamaDrop + lambda(iterNumber, antNum) ))^2;
            pPAnt = dropPAnt(iterNumber, antNum);
            
            randNumber = rand;
            
            % 
            if dropPAnt(iterNumber, antNum) > randNumber
                %drop data
                lattice( ants( antNum ).location(1), ants( antNum ).location(2) ) = ants( antNum ).datum;
                %bDataOnLattice( ants( antNum ).datum ) = 1;
                
                dataOnLattice( ants( antNum ).datum, 1 ) = ants( antNum ).location(1);
                dataOnLattice( ants( antNum ).datum, 2 ) = ants( antNum ).location(2);
                
                pick = 0;
                while ~pick
                    % Random select datum
                    rndData = randi( count_data );
                    if bDataOnLattice( rndData ) == 0
                        continue;
                    end
                    % neighborsAnts[] -- length numOfNeighbors
                    count_neigh = 0;
                    for x = -neighborSize : neighborSize
                        for y = -neighborSize : neighborSize
                            if( x ~= 0 && y ~= 0 && dataOnLattice( rndData, 1 )+x > 0 && dataOnLattice( rndData, 2 )+y > 0 )
                                if( lattice( dataOnLattice( rndData, 1 )+x, dataOnLattice( rndData, 2 )+y ) ~= 0 )
                                    count_neigh = count_neigh + 1;
                                    neighborsData( count_neigh ) = lattice( dataOnLattice( rndData, 1 )+x, dataOnLattice( rndData, 2 )+y );
                                end
                            end
                        end 
                    end

                    % calc distance between curAnt and all their neighbors
                    % d === dist_neighbor
                    d = zeros( count_neigh, 1 );
                    for neighAntIt = 1:count_neigh
                        d(neighAntIt) = distanceMatrix( ants(antNum).datum , neighborsData(neighAntIt) );
                    end

                    % calc f(i)
                    lambda_pick = max( 0, (1/count_neigh^2)*sum(1 - d./alpha) );
                    
                    %Pick up stage
                    pickupPAnt(iterNumber, antNum) = (gamaPick / (gamaPick + lambda_pick) )^2;
                    ppick = pickupPAnt(iterNumber, antNum);
                    
                    randNumber = rand;
                    % TODO
                    
                    if pickupPAnt(iterNumber, antNum) > randNumber
                        pick = 1;
                        bDataOnLattice( ants( antNum ).datum ) = 1;
                        
                        ants( antNum ).datum = rndData;
                        ants( antNum ).location(1) = dataOnLattice( ants( antNum ).datum, 1 );
                        ants( antNum ).location(2) = dataOnLattice( ants( antNum ).datum, 2 );

                        lattice( ants( antNum ).location(1), ants( antNum ).location(2) ) = 0;
                        bDataOnLattice( ants( antNum ).datum ) = 0;        
                        
                    end
                    
                end
            end
             
        end
    end
    
    %---- end for iterNumber
    for antNum = 1:numberOfAnts
        lattice( ants( antNum ).location(1), ants( antNum ).location(2) ) = ants( antNum ).datum;
        bDataOnLattice( ants( antNum ).datum ) = 1;

        dataOnLattice( ants( antNum ).datum, 1 ) = ants( antNum ).location(1);
        dataOnLattice( ants( antNum ).datum, 2 ) = ants( antNum ).location(2);
    end
    
end

