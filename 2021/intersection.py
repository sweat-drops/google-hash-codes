class Intersection:

    id = 0

    in_streets = []

    out_streets = []

    def __init__(self, id):
        self.id = id
        self.in_streets = []
        self.out_streets = []

    def add_in_street(self, street):
        self.in_streets.append(street)

    def add_out_street(self, street):
        self.out_streets.append(street)