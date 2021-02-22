class PizzaGroup:
    teamNumber = 2
    selectedPizzas = []

    ingredientsSet = set()
    worstDelta = 0

    partialSets = []

    def __init__(self, teamNumber, selectedPizzas):
        self.teamNumber = teamNumber
        self.selectedPizzas = selectedPizzas

        self.ingredientsSet = set([ingr for p in selectedPizzas for ingr in p[1].ingr])
        self.calculate_partials()

    def score(self):
        return len(self.ingredientsSet)

    def calculate_partials(self):

        partial_sets = []
        for i in range(0, self.teamNumber):
            partial_sets.append(
                set([ingr for ind, p in enumerate(self.selectedPizzas) if ind != i for ingr in p[1].ingr]))

        self.partialSets = partial_sets
        self.worstDelta = len(self.ingredientsSet) - max([len(x) for x in self.partialSets])

    def valuate_pizza(self, pizzaIdx, pizza, replace=True):
        bestScore = BestScore()  # [idx, value, set, scoreDelta]

        for idx, partialSet in enumerate(self.partialSets):
            newSet = set(self.partialSets[idx])
            newSet.update(pizza.ingr)

            ingredientsDelta = self.selectedPizzas[idx][1].count - pizza.count

            coeff = 1.5 # d => 1.5, c => 1.5
            if len(newSet) + (ingredientsDelta / coeff) > bestScore.score() + (bestScore.ingredientsDelta / coeff):
                bestScore.idx = idx
                bestScore.ingredientsSet = newSet
                bestScore.ingredientsDelta = ingredientsDelta
                bestScore.scoreDelta = len(newSet) - len(self.ingredientsSet)

        if replace:
            self.replace_pizza(pizzaIdx, pizza, bestScore)
        return bestScore

    def replace_pizza(self, pizzaIdx, pizza, bestScore):
        ingredientsDelta = self.selectedPizzas[bestScore.idx][1].count - pizza.count
        if bestScore.scoreDelta + (ingredientsDelta / 2) >= 0:
            self.selectedPizzas[bestScore.idx] = [pizzaIdx, pizza]
            self.ingredientsSet = bestScore.ingredientsSet
            self.calculate_partials()



class BestScore:
    idx = 0
    ingredientsSet = set()
    ingredientsDelta = 0
    scoreDelta = 0

    def score(self):
        return len(self.ingredientsSet)

