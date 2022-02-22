class Client:
    id: int = 0
    likes = set()
    dislikes = set()

    incompatibility: set[int] = set()

    def __init__(self, id) -> None:
        self.id = id
        self.likes = set()
        self.dislikes = set()
        self.incompatibility = set()

    def addLike(self, liked):
        self.likes.add(liked)

    def removeLike(self, liked):
        self.likes.remove(liked)

    def addDislike(self, disliked):
        self.dislikes.add(disliked)

    def removeDislike(self, disliked):
        self.dislikes.remove(disliked)

    def addIncompatibility(self, id):
        self.incompatibility.add(id)

    def score(self, clientRepo):
        if len(self.incompatibility) == 0:
            return -100

        incompatibles = 0
        for clientId in self.incompatibility:
            if clientRepo.has(clientId):
                incompatibles += len(clientRepo.get(clientId).incompatibility)
        return len(self.incompatibility) * 1000 - incompatibles

class ClientRepo:
    
    data: dict[str, Client] = {}

    def __init__(self) -> None:
        data = {}

    def add(self, client: Client) -> bool:
        self.data[client.id] = client

    def has(self, clientId: int) -> bool:
        return clientId in self.data

    def get(self, id: int) -> Client:
        return self.data[id]

    def remove(self, id: int, ingrRepo, ignore: str = "") -> Client:
        client = self.get(id)
        for like in client.likes:
            if like == ignore or not ingrRepo.has(like):
                continue
            ingrRepo.get(like).removeLikedBy(id)

        for dislike in client.dislikes:
            if dislike == ignore or not ingrRepo.has(dislike):
                continue
            ingrRepo.get(dislike).removeDislikedBy(id)

        for incompatible in client.incompatibility:
            if self.has(incompatible):
                self.get(incompatible).incompatibility.remove(id)
        del self.data[id]

    def check_compatibility(self, firstId, secondId):
        first = self.get(firstId)
        second = self.get(secondId)


        for liked in first.likes:
            if liked in second.dislikes:
                return False
        for disliked in first.dislikes:
            if disliked in second.likes:
                return False
        return True

    def score(self):
        score = 0
        for id in self.data:
            if len(self.data[id].likes) == 0:
                score += 1
        return score

class Ingredient:
    name = ""

    likedBy = set()
    dislikedBy = set()

    def __init__(self, name) -> None:
        self.name = name
        self.likedBy = set()
        self.dislikedBy = set()

    def score(self):
        return len(self.likedBy) - len(self.dislikedBy) * 1.1

    def addLikedBy(self, liked):
        self.likedBy.add(liked)

    def removeLikedBy(self, liked):
        self.likedBy.remove(liked)

    def addDislikedBy(self, disliked):
        self.dislikedBy.add(disliked)

    def removeDislikedBy(self, disliked):
        self.dislikedBy.remove(disliked)


class IngrRepo:

    selected = set()
    data: dict[str, Ingredient] = {}

    def __init__(self) -> None:
        selected = set()
        data = {}

    def has(self, name) -> bool:
        return name in self.data

    def add(self, ingr: Ingredient) -> bool:
        self.data[ingr.name] = ingr

    def get(self, name: str) -> Ingredient:
        return self.data[name]

    def select(self, name: str, clientRepo: ClientRepo):
        self.selected.add(name)

        ingr = self.get(name)
        for likedBy in ingr.likedBy:
            client = clientRepo.get(likedBy)
            client.removeLike(name)

        for dislikedBy in ingr.dislikedBy:
            # Questi clienti non saranno MAI soddisfatti
            clientRepo.remove(dislikedBy, self, name)

        del self.data[name]

    def unselect(self, name: str, clientRepo: ClientRepo):
        ingr = self.get(name)
        for likedBy in ingr.likedBy:
            # Questi clienti non verranno mai soddisfatti
            clientRepo.remove(likedBy, self, name)

        for dislikedBy in ingr.dislikedBy:
            client = clientRepo.get(dislikedBy)
            client.removeDislike(name)

        del self.data[name]
        

