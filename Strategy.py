import Player
import Game

class Strategy:

    def __init__(self, player: Player):
        self.player = player

    def next_move(self):
        pass

    @property
    def myLastMove(self):
        return self.player.history[-1][0]

    @property
    def theirLastMove(self):
        return self.player.history[-1][1]



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
        if len(player.history) < 1:
            return 'C'
        else:
            return self.theirLastMove
