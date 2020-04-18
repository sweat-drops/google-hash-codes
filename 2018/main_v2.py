import numpy as np
from timeit import default_timer as timer

filenames = ["A", "B", "C", "D", "E"]
curr_points = [10, 176877, 15805661, 11660274, 21465945]

timeStart = timer()
for file in filenames:
    print("--- START FILE {} ---".format(file))

    # ====================
    # === INPUT PARSER ===
    # ====================
    time = timer()
    rides = []
    maxPoints = 0
    with open("in/{}.in".format(file)) as f:
        R, C, F, N, B, T = map(int, f.readline().split())
        print("R: {}, C: {}, F: {}, N: {}, B:{}, T:{}".format(R, C, F, N, B, T))
        runID = 0
        for r in f.readlines():
            rides.append(list(map(lambda item: int(item), r.split())) + [runID])
            maxPoints += B
            maxPoints += abs(rides[runID][0]-rides[runID][2]) + abs(rides[runID][1]-rides[runID][3])
            runID += 1
    print("CURR_SCORE: {}, MAX_SCORE: {}".format(curr_points[filenames.index(file)], maxPoints))
    
    # initially all vehicles starts from (0, 0)
    vehicles = []
    for v in range(F): 
        vehicles.append([0, 0])
    
    # initially all vehicles are at time 0
    times = np.zeros(F, dtype=int)
    

    # ===================
    # === CALCULATION ===
    # ===================
    points = 0
    vNumber = 0
    vStopped = []
    while len(vStopped) < F:
        v = vehicles[vNumber]
        vT = times[vNumber]
        # If the vehicle can do a ride
        if vT < T:
            bestRidePoints = -1000000
            vRides = rides.copy()
            bestRide = None
            # Filter only rides that the vehicle can complete ontime
            for r in filter(lambda r: (vT + abs(v[0]-r[0]) + abs(v[1]-r[1]) + abs(r[0]-r[2]) + abs(r[1]-r[3])) <= r[5], vRides):
                # Parameters
                a, b = [0, 1]
                if file == 'C': a = 0.1
                if file == 'D': a = 0.2

                # Select the ride i can start first
                ridePoints = -a*(abs(r[0]-r[2]) + abs(r[1]-r[3])) - max(abs(v[0]-r[0]) + abs(v[1]-r[1]), r[4]-vT)
                if r[4] - vT >= abs(v[0]-r[0]) + abs(v[1]-r[1]):
                    ridePoints -= b*B

                if ridePoints > bestRidePoints:
                    bestRide = r
                    bestRidePoints = ridePoints
            # If has been found at least one ride 
            if bestRide is not None:
                # Add points
                points += abs(bestRide[0]-bestRide[2]) + abs(bestRide[1]-bestRide[3])
                if bestRide[4] - vT >= abs(v[0]-bestRide[0]) + abs(v[1]-bestRide[1]):
                    points += B
                # Add ride id to vehicle
                vehicles[vNumber].append(bestRide[6])
                # Update timestamp
                times[vNumber] += max(abs(v[0]-bestRide[0]) + abs(v[1]-bestRide[1]), bestRide[4]-vT) + abs(bestRide[0]-bestRide[2]) + abs(bestRide[1]-bestRide[3])
                # Update vehicle coordinates
                vehicles[vNumber][0] = bestRide[2]
                vehicles[vNumber][1] = bestRide[3]
                # Remove ride from list
                rides.remove(bestRide)
                del bestRide
                # Go to the next vehicle
                if vNumber == F - 1: vNumber = 0
                else: vNumber += 1
            # If there isn't a ride for that vehicle, stop it
            else:
                vStopped.append(vNumber)
                if vNumber == F - 1: vNumber = 0
                else: vNumber += 1
    
    print("Scored: {}".format(points))
    print("Unassigned rides: {}".format(len(rides)))
    if points > curr_points[filenames.index(file)]: print("New max found")

    # ==============
    # === OUTPUT ===
    # ==============
    with open("out/{}.out".format(file), 'w') as f:
        for v in vehicles:
            v = v[2:]
            f.write("{} ".format(len(v)))
            for r in v:
                f.write("{} ".format(r))
            f.write("\n")
    print("--- END file {} in {}--\n".format(file, timer()-time))

print("ENDED ALL FILES in {}".format(timer()-timeStart))