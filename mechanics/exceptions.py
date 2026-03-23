class Good(Exception):pass

class Bad(Exception):
    def __init__(self, current, damage):
        self.current = current
        self.damage = damage

class UnknownVariable(Bad):
    def __int__(self, current):
        super().__init__(current, 1)

    def __str__(self):
        return 'один из операндов - неизвестная переменная'
    
class WrongPriority(Bad):
    def __init__(self, current):
        super().__init__(current, 1)

    def __str__(self):
        return 'не тот порядок действий'
    
class NoCommutativity(Bad):
    def __init__(self, current):
        super().__init__(current, 2)

    def __str__(self):
        return 'у этого элемента нет коммутативности'