class Guy:
    def __init__(self, name) -> None:
        self.name = name
        self.skills = {}

    def add_skill(self, name, level):
        self.skills[name] = level
    
    def improve_skill(self, name):
        if not name in self.skills:
            self.skills[name] = 0
        self.skills[name] += 1
        
    def __str__(self) -> str:
        return f"{self.name}, {self.skills}"

class Project:
    def __init__(self, name, days, score, before) -> None:
        self.name = name
        self.days = days
        self.score = score
        self.before = before
        self.selected = False
        self.required = []
        self.mentored = set()

    def add_role(self, skill, level):
        self.required.append({ 'skill': skill, 'level': level})

    def score_at_t(self, t):
        if self.selected:
            return -1000
        actual_score = self.score + min(0, self.before - (t + self.days))

        is_late =  (((self.before - self.days) - t) / self.days) + 1

        return (actual_score / self.days) / len(self.required) / is_late


    
