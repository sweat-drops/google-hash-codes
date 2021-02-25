from street import Street
from car import Car
from intersection import Intersection

#file_names = ['c']
file_names = ['a', 'b', 'c', 'd', 'e', 'f']

for file_name in file_names:
    print(f"--- START FILE {file_name} ---")

    input_file_name = f"in/{file_name}.txt"
    output_file_name = f"{file_name}.out"

    in_file = open(input_file_name, 'r')
    out_file = open(output_file_name, 'w+')

    T, I, S, V, F = map(int, in_file.readline().split())

    print(f"T={T} I={I} S={S} V={V} F={F}")

    streets = {}
    streets_map = {}

    intersections = {}

    i = S
    while i > 0:
        street = Street(i, in_file.readline())
        streets[i] = street
        streets_map[street.name] = street.id

        if street.fr not in intersections:
            intersections[street.fr] = Intersection(street.fr)
        intersections[street.fr].add_out_street(street)

        if street.to not in intersections:
            intersections[street.to] = Intersection(street.to)
        intersections[street.to].add_in_street(street)

        i -= 1

    cars = []
    for i, line in enumerate(in_file.readlines()):
        words = line.split()

        car_streets_names = words[1:]
        car_streets = []

        for car_street_name in car_streets_names:
            actual_street = streets[streets_map[car_street_name]]
            actual_street.add_car()
            car_streets.append(actual_street)

        cars.append(Car(i, int(words[0]), car_streets))

    outputs = []
    score = 0

    for intersection in intersections.values():
        valid_streets = [s for s in intersection.in_streets if s.car_total > 0]
        valid_streets.sort(key=lambda x: x.car_total, reverse=True)
        if (len(valid_streets) > 0):
            outputs.append([intersection.id, valid_streets])

    total_car_per_intersection = {}

    for key, intersection in intersections.items():
        total_car_per_intersection[key] = sum([s.car_total for s in intersection.in_streets])


    # Calc outputs & score
    out_file.write(f"{len(outputs)}\n")
    for output in outputs:
        intersection_id = output[0]
        intersection = intersections[intersection_id]
        
        # total_car_per_intersection = sum([s.total_car for s in intersection.in_street])
        
        totals = sum([s.car_total for s in output[1]])
        cycle_time = max(1, totals / 10)
        #avg_intersections = sum([len(c.streets) for c in cars]) / len(cars)
        #avg_street_in = sum([len(intersection.in_streets) for intersection in intersections.values()]) / len(intersections)

        out_file.write(f"{output[0]}\n")
        out_file.write(f"{len(output[1])}\n")
        for street in output[1]:
            out_file.write(f"{street.name} {max(1, int(street.car_total * cycle_time / totals))}\n")

