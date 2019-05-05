import Strategy


class Player:
    """Player class - uses one strategy to compete in games.

    >>> p1 = Player(strategy=Strategy.AlwaysCooperate)
    >>> p1.name
    'P1'
    >>> p1.history = [('C', 'D')]
    >>> p1.myLastMove
    'C'
    >>> p1.theirLastMove
    'D'
    >>> p1.has_recently_defected(1)
    True
    >>> p1.has_defected_for(1)
    True
    """
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

        # Stats for use by Strategy's next_move() function
        self.defectionCountdown = 0
        self.cooperationCountdown = 0
        self.defectionCount = 0
        self.cooperationCount = 0


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


    def has_defected_for(self, pastrounds):
        roundcount = 0
        for round in self.history[-pastrounds:]:
            if round[1] == 'D':
                roundcount += 1
        if roundcount == pastrounds:
            return True
        else:
            return False


