from timeit import default_timer as timer

filenames = ["A", "B", "C", "D", "E"]
curr_points = [10, 175452, 15805661, 11681464, 21401945]

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

    # initially all vehicles starts from (0, 0)
    vehicles = []
    for v in range(F): 
        vehicles.append([0, 0])

    print("Max points for dataset {}: {}".format(file, maxPoints))

    # ===================
    # === CALCULATION ===
    # ===================
    points = 0
    for v in vehicles:
        t = 0
        while t < T:
            bestRidePoints = -1000000
            vRides = rides.copy()
            bestRide = None
            # Filter only rides that the vehicle can complete ontime
            for r in filter(lambda r: (t + abs(v[0]-r[0]) + abs(v[1]-r[1]) + abs(r[0]-r[2]) + abs(r[1]-r[3])) <= r[5], vRides):
                # parameters
                a, b = [0, 1]
                if file == 'B': a = 33
                if file == 'D': a = 0.25
                if file == 'E': b = 100
                
                # Select the ride i can start first
                ridePoints = -a*(abs(r[0]-r[2]) + abs(r[1]-r[3])) - max(abs(v[0]-r[0]) + abs(v[1]-r[1]), r[4] - t)

                if r[4] - t >= abs(v[0]-r[0]) + abs(v[1]-r[1]):
                    ridePoints += b*B

                if ridePoints >= bestRidePoints:
                    bestRide = r
                    bestRidePoints = ridePoints

            if not bestRide == None:
                points += abs(bestRide[0]-bestRide[2]) + abs(bestRide[1]-bestRide[3])
                if bestRide[4] - t >= abs(v[0]-bestRide[0]) + abs(v[1]-bestRide[1]):
                    points += B

                # Add ride id to vehicle
                v.append(bestRide[6])
                # Update timestamp
                t += max(abs(v[0]-bestRide[0]) + abs(v[1]-bestRide[1]), bestRide[4] - t) + abs(bestRide[0]-bestRide[2]) + abs(bestRide[1]-bestRide[3])
                # Update vehicle coordinates
                v[0] = bestRide[2]
                v[1] = bestRide[3]
                # Remove ride from list
                rides.remove(bestRide)
                del bestRide
            else:
                break
    print("SCORED: {} with a {} e b {}".format(points, a, b))
    print("Unassigned rides: {}".format(len(rides)))    


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
    print("--- END file {} --\n".format(file))

print("ENDED ALL FILES in {}".format(timer()-timeStart))