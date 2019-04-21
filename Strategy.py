import Player
import Game

class Strategy:

    def __init__(self):
        pass

    def next_move(self):
        self.myLastMove = Player.history[-1][0]
        self.theirLastMove = Player.history[-1][1]
        pass


class AlwaysCooperate(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'AlwaysCooperate'

    def next_move(self):
        return 'C'


class AlwaysDefect(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'AlwaysDefect'

    def next_move(self):
        return 'D'


class TitForTat(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'TitForTat'

    def next_move(self):
        if len(Player.history) < 1:
            return 'C'
        else:
            return self.theirLastMove
