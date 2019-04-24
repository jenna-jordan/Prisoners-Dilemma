class Strategy:

    def __init__(self):

        if self.__class__.__name__ == 'Strategy':
            raise Exception("Base class Strategy should not be called, call a specific strategy subclass instead.")
        else:
            pass

    def next_move(self, player):
        pass


class AlwaysCooperate(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'AlwaysCooperate'

    def next_move(self, player):
        return 'C'


class AlwaysDefect(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'AlwaysDefect'

    def next_move(self, player):
        return 'D'


class TitForTat(Strategy):

    def __init__(self):
        super().__init__()
        self.name = 'TitForTat'

    def next_move(self, player):
        if player.history:
            return player.theirLastMove
        else:
            return 'C'
