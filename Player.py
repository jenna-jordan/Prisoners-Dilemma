import Strategy


class Player:

    playerCount = 0

    def __init__(self, strategy: Strategy, name=None):

        self.strategy = strategy

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





