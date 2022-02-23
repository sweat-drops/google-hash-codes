#!/usr/local/bin/python3

import copy
from data import Client, ClientRepo, IngrRepo, Ingredient
import sys
import random
import threading

if len(sys.argv) <= 1:
    print("Manca il tipo di calcolo ('client', 'ingr)")
    exit(1)

if len(sys.argv) <= 2:
    print("Manca il nome del file (a,b,c,d,e)")
    exit(1)

fileName = sys.argv[2]
type = sys.argv[1]

print(f"--- START FILE {fileName} ---")

inputFileName = f"in/{fileName}.in"
outputFileName = f"{fileName}.out"

inFile = open(inputFileName, 'r')
outFile = open(outputFileName, 'w+')

C, = map(int, inFile.readline().split())

ingrRepo = IngrRepo()
clientRepo = ClientRepo()

for i in range(0, C):
    client = Client(i)
    clientRepo.add(client)

    likedIngrs = inFile.readline().split()[1:]
    dislikedIngrs = inFile.readline().split()[1:]

    for liked in likedIngrs:
        if not ingrRepo.has(liked):
            newIngr = Ingredient(liked)
            ingrRepo.add(newIngr)

        ingr = ingrRepo.get(liked)
        ingr.addLikedBy(client.id)
        client.addLike(ingr.name)
    
    for disliked in dislikedIngrs:
        if not ingrRepo.has(disliked):
            newIngr = Ingredient(disliked)
            ingrRepo.add(newIngr)

        ingr = ingrRepo.get(disliked)
        ingr.addDislikedBy(client.id)
        client.addDislike(ingr.name)

def copy_repos():
    origClients = copy.deepcopy(clientRepo.data)
    origIngrs = copy.deepcopy(ingrRepo.data)

    origClientsRepo = ClientRepo()
    origClientsRepo.data = origClients

    origIngrRepo = IngrRepo()
    origIngrRepo.data = origIngrs

    return (origIngrRepo, origClientsRepo)

origIngrRepo, origClientsRepo = copy_repos()

def select_by_ingredients():

    while True:
        ingredients = list(ingrRepo.data.values())
        ingredients = sorted(ingredients, key= lambda x: x.score(), reverse=True)

        if len(ingredients) == 0:
            break

        best = ingredients[0]
        worst = ingredients[-1]

        if len(ingredients) > 1 and worst.score() < 0:
            ingrRepo.unselect(worst.name, clientRepo)

        if best.score() >= 0:
            ingrRepo.select(best.name, clientRepo)
        else:
            break
         
        if len(ingredients) > 2 and ingredients[1].score() >= 1:
            ingrRepo.select(ingredients[1].name, clientRepo)

def select_by_clients():
    while True:
        validClients = [x for x in clientRepo.data.values() if len(x.likes) > 0]

        if len(validClients) < 1:
            break

        client = sorted(validClients, key= lambda x: x.score(clientRepo=clientRepo), reverse=False)[0]

        for liked in list(client.likes):
            ingrRepo.select(liked, clientRepo=clientRepo)
        for disliked in list(client.dislikes):
            ingrRepo.unselect(disliked, clientRepo=clientRepo)

def write_output(selected):
    outFile.truncate(0)
    outFile.seek(0)
    outFile.write(f"{len(selected)} {' '.join(selected)}\n")

def reset_original(origClients, origIngr):
    clientRepo.data = copy.deepcopy(origClients.data)
    ingrRepo.data = copy.deepcopy(origIngr.data)
    ingrRepo.selected = []

def calc_score(origClientRepo, selected):
    score = 0
    for client in origClientRepo.data.values():
        if is_satisfied(client, selected):
            score = score + 1
    return score

def is_satisfied(client: Client, selected):
    for liked in client.likes:
        if not liked in selected:
            return False
    for disliked in client.dislikes:
        if disliked in selected:
            return False
    return True

def client_swipe(client, data, lock = None):
    tempSelected = copy.deepcopy(data['selected'])

    if not is_satisfied(client, data['selected']):
        # Lo aggiungo
        for liked in client.likes:
            tempSelected.add(liked)

        for disliked in client.dislikes:
            if disliked in tempSelected:
                tempSelected.remove(disliked)
    else:
        # Lo rimuovo
        for liked in client.likes:
            if liked in tempSelected:
                tempSelected.remove(liked)

        #for disliked in client.dislikes:
        #    tempSelected.add(disliked)
    
    tempScore = calc_score(origClientsRepo, tempSelected)

    if tempScore >= data['score']:
        isMax = tempScore > data['score']
        if lock != None:
            lock.acquire()
        
        if isMax or random.random() > 0.5:
            data['score'] = tempScore
            data['selected'] = tempSelected

        if isMax:
            print(f"NUOVO MAX: {data['score']}")
            write_output(data['selected'])
        if lock != None:
            lock.release()

def ingredient_swipe(ingr, data, lock = None):
    tempSelected = copy.deepcopy(data['selected'])

    if not ingr in tempSelected:
        tempSelected.add(ingr)
    else:
        tempSelected.remove(ingr)

    tempScore = calc_score(origClientsRepo, tempSelected)

    if tempScore >= data['score']:
        isMax = tempScore > data['score']
        if lock != None:
            lock.acquire()
        
        if isMax or random.random() > 0.5:
            data['score'] = tempScore
            data['selected'] = tempSelected

        if isMax:
            print(f"NUOVO MAX: {data['score']}")
            write_output(data['selected'])
        if lock != None:
            lock.release()


def swipe_clients(selected, score):
    clientIds =  list(origClientsRepo.data.keys())

    ingredients =  list(origIngrRepo.data.keys())

    data = { 'selected': selected, 'score': score}

    while True:
        completed = True
        random.shuffle(clientIds)

        lock = threading.Lock()
        
        i = 0
        while i < len(clientIds):
            if i > 0 and i % 500 == 0:
                print(f"{data['score']}\t{i}/{C} Clients")

            threads = []

            for _ in range(0, 10):
                if i < len(clientIds):
                    th = threading.Thread(target=client_swipe, args=(origClientsRepo.get(clientIds[i]), data, lock))
                    th.start()
                    threads.append(th)
                    i = i + 1
            for th in threads:
                th.join()


        random.shuffle(ingredients)
        i = 0
        while i < len(ingredients):
            if i > 0 and i % 500 == 0:
                print(f"{data['score']}\t{i}/{I} Ingredients")

            threads = []

            for _ in range(0, 10):
                if i < len(ingredients):
                    th = threading.Thread(target=ingredient_swipe, args=(ingredients[i], data, lock))
                    th.start()
                    threads.append(th)
                    i = i + 1
            for th in threads:
                th.join()

        #if completed:
        #    print(f"Completed {score}")
        #    break
    return selected, score

def double_swipe_clients(selected, score):
    clientIds =  list(origClientsRepo.data.keys())
    random.shuffle(clientIds)

    for i in range(0, len(clientIds) - 1):
        client = clientIds[i]
        tempSelected = copy.deepcopy(selected)

        if i > 0 and i % 100 == 0:
                print(f"{score}\t{i}/{C} double swap Clients")

        if not clientRepo.has(client):
            # Lo aggiungo
            for liked in origClientsRepo.get(client).likes:
                if not liked in tempSelected:
                    tempSelected.add(liked)

            for disliked in origClientsRepo.get(client).dislikes:
                if disliked in tempSelected:
                    tempSelected.remove(disliked)
        else:
            # Lo rimuovo
            for liked in origClientsRepo.get(client).likes:
                if liked in tempSelected:
                    tempSelected.remove(liked)

            for disliked in origClientsRepo.get(client).dislikes:
                if not disliked in tempSelected:
                    tempSelected.add(disliked)

        for j in range(i+1, len(clientIds)):
            lastTempSelected = copy.deepcopy(tempSelected)

            secondClient = clientIds[j]

            if not clientRepo.has(secondClient):
                # Lo aggiungo
                for liked in origClientsRepo.get(secondClient).likes:
                    if not liked in tempSelected:
                        lastTempSelected.add(liked)

                for disliked in origClientsRepo.get(secondClient).dislikes:
                    if disliked in tempSelected:
                        lastTempSelected.remove(disliked)
            else:
                # Lo rimuovo
                for liked in origClientsRepo.get(secondClient).likes:
                    if liked in tempSelected:
                        lastTempSelected.remove(liked)

                for disliked in origClientsRepo.get(secondClient).dislikes:
                    if not disliked in tempSelected:
                        lastTempSelected.add(disliked)
            tempScore = calc_score(origClientsRepo, lastTempSelected)
            if tempScore > score:
                selected = lastTempSelected
                score = tempScore
            
                print(f"NUOVO MAX: {score}")
                write_output(selected)
                break
    
    print(f"FINAL: {score}")
    return selected, score

I = len(origIngrRepo.data)

print(f"C: {C}, I: {I}")

target = 0
if type == 'ingr':
    select_by_ingredients()

else:
    # Select by clients
    clientIds = list(clientRepo.data.keys())

    for i in range(0, len(clientIds) - 1):
        for j in range(i+1,len(clientIds)):
            compatible = clientRepo.check_compatibility(clientIds[i], clientIds[j])

            if not compatible:
                clientRepo.get(clientIds[i]).addIncompatibility(clientIds[j])
                clientRepo.get(clientIds[j]).addIncompatibility(clientIds[i])

    print(f"Controllo compatibilità effettuato")

    origIngrRepo, origClientsRepo = copy_repos()

    select_by_clients()

score = calc_score(origClientsRepo, ingrRepo.selected)
print(f"Score {score}, usati {len(ingrRepo.selected)} ingr")
selected, score = swipe_clients(ingrRepo.selected, score)

selected, score = double_swipe_clients(ingrRepo.selected, score)
