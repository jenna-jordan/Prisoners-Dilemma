import Strategy
import Game

class Player:

    playerCount = 0
    playerList = []

    def __init__(self, strategy: Strategy, name=None):

        # strategy must be a Strategy subclass
        self.strategy = strategy

        # keep track of how many strategies there are
        Player.playerCount += 1
        # add player to list of all players
        Player.playerList.append(self)

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

