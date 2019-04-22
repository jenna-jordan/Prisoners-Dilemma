class Strategy:

    def __init__(self):
        pass

    def next_move(self, player_history):
        pass

    # @property
    # def myLastMove(self):
    #     return self[-1][0]
    #
    # @property
    # def theirLastMove(self):
    #     return self[-1][1]

class AlwaysCooperate(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'AlwaysCooperate'

    def next_move(self, player_history):
        return 'C'


class AlwaysDefect(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'AlwaysDefect'

    def next_move(self, player_history):
        return 'D'


class TitForTat(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'TitForTat'

    def next_move(self, player_history):
        if player_history:
            return player_history[-1][1]
        else:
            return 'C'
