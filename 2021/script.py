
file_name = 'c'

print(f"--- START FILE {file_name} ---")

input_file_name = f"in/{file_name}.in"
output_file_name = f"out/{file_name}.out"

in_file = open(input_file_name, 'r')
out_file = open(output_file_name, 'w+')

X, Y, Z = map(int, in_file.readline().split())

print(f"X={X} Y={Y} Z={Z}")

data = []

i = 0
for line in in_file.readlines():
    obj_name = line.split()
    # Init stuff with object
    data.append(obj_name)
    i += 1

outputs = []
score = 0

# Calc outputs & score
out_file.write(f"{len(outputs)}\n")
for output in outputs:
    out_file.write(f"{len(output)} {' '.join([p.i for p in output])}\n")

