import Strategy


class Player:

    playerCount = 0

    def __init__(self, strategy: Strategy, name=None):

        self.strategy = strategy()

        Player.playerCount += 1
        if name is None:
            self.name = "P{}".format(Player.playerCount)
        else:
            self.name = name

        # Tournament-level stats
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.points = 0

        # Game-level stats
        self.history = []

    @property
    def myLastMove(self):
        return self.history[-1][0]

    @property
    def theirLastMove(self):
        return self.history[-1][1]

    def has_recently_defected(self, pastrounds):
        for round in self.history[-pastrounds:]:
            if round[1] == 'D':
                return True
        return False





