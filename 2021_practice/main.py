from pizza import Pizza
from pizza_group import PizzaGroup


def best_pizza_group_by_members(pizzas, teamNumber):
    # Selezione delle pizze da assegnare al team in formato [indicePizzas, oggettoPizza]
    selectedPizzas = [[0, pizzas[0]], [1, pizzas[1]]]  # Parto sempre dalla prima

    if teamNumber >= 3:
        selectedPizzas.append([2, pizzas[2]])
    if teamNumber >= 4:
        selectedPizzas.append([3, pizzas[3]])

    pizza_group = PizzaGroup(teamNumber, selectedPizzas)

    j = teamNumber
    while j < len(pizzas):
        idx = j
        j = j + 1

        if pizzas[idx].count * 1.1 < pizza_group.worstDelta:
            break
        if pizzas[idx].count == pizza_group.worstDelta and pizzas[idx].count == 1:
            break

        pizza_group.valuate_pizza(idx, pizzas[idx])

    return pizza_group


fileNames = ['e']

for fileName in fileNames:
    print(f"--- START FILE {fileName} ---")

    inputFileName = f"in/{fileName}.in"
    outputFileName = f"{fileName}.out"

    inFile = open(inputFileName, 'r')
    outFile = open(outputFileName, 'w+')

    M, T2, T3, T4 = map(int, inFile.readline().split())

    print(f"M={M} T2={T2} T3={T3} T4={T4}")

    pizzas = []
    i = 0
    for line in inFile.readlines():
        newPizza = Pizza(i, line)
        pizzas.append(newPizza)
        i = i + 1

    pizzas.sort(key=lambda x: x.count, reverse=True)

    print(f"Import file {fileName} completed")

    outputs = []

    score = 0
    totalPizzas = 0
    teamsMissing = {
        '2': T2,
        '3': T3,
        '4': T4
    }

    bestScores = {
        '2': best_pizza_group_by_members(pizzas, 2).score(),
        '3': best_pizza_group_by_members(pizzas, 3).score(),
        '4': 0
    }
    i = 0

    while i < (T2 + T3 + T4):
        if i > 0 and i % 250 == 0:
            print(
                f"Team n°{i}/{T2 + T3 + T4} - score {score} using {totalPizzas} pizzas - Missing teams T4:{teamsMissing['4']} T3:{teamsMissing['3']} T2:{teamsMissing['2']}")
        i = i + 1

        teamNumber = 4
        pizzaGroup = []

        if teamsMissing['4'] > 0 and len(pizzas) >= 4:
            pizzaGroup = best_pizza_group_by_members(pizzas, 4)
            bestScores['4'] = pizzaGroup.score()

            if bestScores['3'] >= bestScores['4']:
                otherGroup = best_pizza_group_by_members(pizzas, 3)
                bestScores['3'] = otherGroup.score()

                if bestScores['3'] >= bestScores['4'] and teamsMissing['3'] > 0:
                    teamNumber = 3
                    pizzaGroup = otherGroup

                if bestScores['2'] >= bestScores['3']:
                    anotherGroup = best_pizza_group_by_members(pizzas, 2)
                    bestScores['2'] = anotherGroup.score()

                    if bestScores['2'] >= bestScores['3'] and teamsMissing['2'] > 0:
                        teamNumber = 2
                        pizzaGroup = anotherGroup

        elif teamsMissing['3'] > 0 and len(pizzas) >= 3:
            teamNumber = 3
            pizzaGroup = best_pizza_group_by_members(pizzas, 3)
            bestScores['3'] = pizzaGroup.score()

            if bestScores['2'] >= bestScores['3']:
                anotherGroup = best_pizza_group_by_members(pizzas, 2)
                bestScores['2'] = anotherGroup.score()

                if bestScores['2'] >= bestScores['3'] and teamsMissing['2'] > 0:
                    teamNumber = 2
                    pizzaGroup = anotherGroup

        elif teamsMissing['2'] > 0 and len(pizzas) >= 2:
            teamNumber = 2
            pizzaGroup = best_pizza_group_by_members(pizzas, 2)

        else:
            break

        # Conversione dell'oggetto selectedPizzas in output
        teamsMissing[str(teamNumber)] -= 1
        outputs.append([x[1] for x in pizzaGroup.selectedPizzas])
        score += len(pizzaGroup.ingredientsSet) ** 2
        totalPizzas = totalPizzas + teamNumber

        # Rimuovo dalla lista le pizze utilizzate
        pizzas = [p for ind, p in enumerate(pizzas) if ind not in [x[0] for x in pizzaGroup.selectedPizzas]]

    print(f"{fileName} completed, estimated score {score}. {totalPizzas} pizzas used from a maximum of {2 * T2 + 3 * T3 + 4 * T4} to send and {M} availables")

    outFile.write(f"{len(outputs)}\n")
    for output in outputs:
        outFile.write(f"{len(output)} {' '.join([p.i for p in output])}\n")
