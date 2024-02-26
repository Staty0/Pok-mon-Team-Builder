class Pokemon:
    def __init__(self, name, types, abilities, formats, hp, attack, defense, speed, special_attack, special_defense):
        self.name = name
        self.types = types
        self.abilities = abilities
        self.formats = formats
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.movepool = []
        self.roles = []

    def add_move(self, move):
        # Add a move to the movepool
        self.movepool.append(move)