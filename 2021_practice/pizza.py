class Pizza:

    i = 0
    ingr = []
    count = 0

    def __init__(self, index, line):
        lineSplit = line.split()
        count, ingredients = lineSplit[0], lineSplit[1:]

        self.i = str(index)
        self.ingr = sorted(ingredients)
        self.count = int(count)

    def __str__(self):
        return f"I:{self.i}, count={self.count}, ingr={self.ingr}"
