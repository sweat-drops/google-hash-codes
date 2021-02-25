class Street:
    id = 0
    name = ''
    value = 0

    fr = 0
    to = 0

    car_total = 0

    def __init__(self, id, line):
        self.id = id

        fr, to, name, value = line.split()

        self.fr = int(fr)
        self.to = int(to)
        self.name = name
        self.value = int(value)

    def add_car(self):
      self.car_total += 1