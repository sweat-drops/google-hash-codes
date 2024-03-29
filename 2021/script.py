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

    outputs = [] # [id, [[streetName, seconds]]]
    score = 0

    max_seconds = 5

    for intersection in intersections.values():
        valid_streets = [s for s in intersection.in_streets if s.car_total > 0]
        valid_streets.sort(key=lambda x: x.car_total, reverse=True)

        total_cars = sum([s.car_total for s in intersection.in_streets])
        if total_cars == 0:
            continue

        selected_streets = []
        for street in intersection.in_streets:
            if street.car_total == 0:
                continue

            perc = street.car_total / total_cars
            seconds = int(perc * max_seconds + 1)

            if seconds > 0:
                selected_streets.append([street.name, seconds])

        for n in range(int(max_seconds / 2), 0, -1):
            all_divisible = True

            for selected_street in selected_streets:
                if selected_street[1] % n != 0:
                    all_divisible = False
                    break
            
            if all_divisible:
                for i, selected_street in enumerate(selected_streets):
                    selected_streets[i] = [ selected_street[0], int(selected_street[1] / n)]

        if (len(selected_streets) > 0):
            outputs.append([intersection.id, selected_streets])

    # Calc outputs & score
    out_file.write(f"{len(outputs)}\n")
    for output in outputs:
        out_file.write(f"{output[0]}\n")
        out_file.write(f"{len(output[1])}\n")
        for street in output[1]:
            out_file.write(f"{street[0]} {street[1]}\n")

# calculate score

# for file_name in file_names:
#     with open('in/' + file_name + '.txt', 'r') as in_f:
#         with open(file_name + '.out', 'r') as out_f:
#             duration, n_intersections, n_streets, n_cars, prize = map(int, in_file.readline().split())
#             n_intersections_out = int(f_out.readlines())
            
