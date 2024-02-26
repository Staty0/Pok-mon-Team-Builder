class Move:
    def __init__(self, name, PP, split, power, type, accuracy, effectDesc, priority):
        self.name = name
        self.PP = PP
        self.split = split
        self.power = power
        self.type = type
        self.accuracy = accuracy
        self.priority = priority
        self.effectDesc = effectDesc
        self.role = []