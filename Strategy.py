import random

class Strategy:
    """Superclass of all strategies. For a list of all strategies refer to:
    http://www.prisoners-dilemma.com/strategies.html
    """
    def __init__(self):

        if self.__class__.__name__ == 'Strategy':
            raise Exception("Base class Strategy should not be called, call a specific strategy subclass instead.")
        else:
            pass

    def next_move(self, player):
        pass


# Basic Strategies

class AlwaysCooperate(Strategy):
    """Cooperates on every move."""
    def __init__(self):
        super().__init__()
        self.name = 'Always Cooperate'
        self.id = 'AllC'

    def next_move(self, player):
        return 'C'


class AlwaysDefect(Strategy):
    """Defects on every move."""
    def __init__(self):
        super().__init__()
        self.name = 'Always Defect'
        self.id = 'AllD'

    def next_move(self, player):
        return 'D'


class Random(Strategy):
    """Makes a random move."""
    def __init__(self):
        super().__init__()
        self.name = 'Random'
        self.id = 'RAND'

    def next_move(self, player):
        return random.choice(['D', 'C'])


# Tit for Tat Strategies

class TitForTat(Strategy):
    """Cooperates on the first move, then copies the opponent’s last move."""
    def __init__(self):
        super().__init__()
        self.name = 'Tit For Tat'
        self.id = 'TFT'

    def next_move(self, player):
        if player.history:
            return player.theirLastMove
        else:
            return 'C'


class TitForTwoTats(Strategy):
    """Cooperates on the first move, and defects only when the opponent defects two times."""
    def __init__(self):
        super().__init__()
        self.name = 'Tit for Two Tats'
        self.id = 'TFTT'

    def next_move(self, player):
        if player.history:
            if player.has_defected_for(2):
                return 'D'
            else:
                return 'C'
        else:
            return 'C'


class TwoTitsForTat(Strategy):
    """Same as Tit for Tat except that it defects twice when the opponent defects."""
    def __init__(self):
        super().__init__()
        self.name = 'Two Tits for Tat'
        self.id = 'TTFT'

    def next_move(self, player):
        if player.history:
            if player.movesCountdown:
                player.movesCountdown -= 1
                return 'D'
            if player.theirLastMove == 'D':
                player.movesCountdown = 1
                return 'D'
            else:
                return 'C'
        else:
            player.movesCountdown = 0  # reset moves countdown at start of each game
            return 'C'


class FirmButFair(Strategy):
    """Cooperates on the first move, and cooperates except after receiving a sucker payoff."""
    def __init__(self):
        super().__init__()
        self.name = 'Firm But Fair'
        self.id = 'FBF'

    def next_move(self, player):
        #TODO


class SuspiciousTitForTat(Strategy):
    """Same as TFT, except that it defects on the first move."""
    def __init__(self):
        super().__init__()
        self.name = 'Suspicious Tit For Tat'
        self.id = 'STFT'

    def next_move(self, player):
        #TODO


class HardTitForTat(Strategy):
    """Cooperates on the first move, and defects if the opponent has defects on any of the previous three moves,
    else cooperates."""
    def __init__(self):
        super().__init__()
        self.name = 'Hard Tit For Tat'
        self.id = 'HTFT'

    def next_move(self, player):
        #TODO


class ReverseTitForTat(Strategy):
    """It does the reverse of TFT.
    It defects on the first move, then plays the reverse of the opponent’s last move."""
    def __init__(self):
        super().__init__()
        self.name = 'Reverse Tit for Tat'
        self.id = 'RTFT'

    def next_move(self, player):
        #TODO

# Punishing Strategies

class GrimTrigger(Strategy):
    """Cooperates, until the opponent defects, and thereafter always defects."""
    def __init__(self):
        super().__init__()
        self.name = 'Grim Trigger'
        self.id = 'GRIM'

    def next_move(self, player):
        if player.history:
            if player.has_recently_defected(len(player.history)):
                return 'D'
            else:
                return 'C'
        else:
            return 'C'


class SoftGrudger(Strategy):
    """Like GRIM except that the opponent is punished with D,D,D,D,C,C."""
    def __init__(self):
        super().__init__()
        self.name = 'Soft Grudger'
        self.id = 'SGRIM'

    def next_move(self, player):
        #TODO

class Gradual(Strategy):
    """Cooperates on the first move, and cooperates as long as the opponent cooperates.
    After the first defection of the other player, it defects one time and cooperates two times;
    After the nth defection it reacts with n consecutive defections
    and then calms down its opponent with two cooperations."""
    def __init__(self):
        super().__init__()
        self.name = 'Gradual'
        self.id = 'GRAD'

    def next_move(self, player):
        if player.history:

            # check countdowns, start countdowns if needed (other player plays 'D')
            if not player.cooperationCountdown and not player.defectionCountdown:
                if player.theirLastMove == 'D':
                    player.defectionCount += 1
                    player.defectionCountdown = player.defectionCount
                    player.cooperationCountdown = 2
                    print(player.defectionCount, "# defects")
                elif player.theirLastMove == 'C':
                    return 'C'

            # when 'D' punishment is in effect
            if player.defectionCountdown:
                print(player.defectionCountdown, '# defects left')
                player.defectionCountdown -= 1
                return 'D'
            # two 'C' forgiveness
            else:
                print(player.cooperationCountdown, '# coops left')
                player.cooperationCountdown -= 1
                return 'C'

        else:
            # reset countdowns at start of each game
            player.defectionCount = 0
            player.defectionCountdown = 0
            player.cooperationCountdown = 0
            return 'C'


# Opportunistic Strategies

class Pavlov(Strategy):
    """Cooperates on the first move.
    If a reward or temptation payoff is received in the last round then repeats last choice,
    otherwise chooses the opposite choice."""
    def __init__(self):
        super().__init__()
        self.name = 'Pavlov'
        self.id = 'PAV'

    def next_move(self, player):
        #TODO


class SoftMajority(Strategy):
    """Cooperates on the first move, and cooperates as long as the number of times the opponent has cooperated
    is greater than or equal to the number of times it has defected, else it defects."""
    def __init__(self):
        super().__init__()
        self.name = 'Soft Majority'
        self.id = 'SM'

    def next_move(self, player):
        #TODO


class HardMajority(Strategy):
    """Defects on the first move, and defects if the number of defections of the opponent
    is greater than or equal to the number of times it has cooperated, else cooperates. """
    def __init__(self):
        super().__init__()
        self.name = 'Hard Majority'
        self.id = 'HM'

    def next_move(self, player):
        #TODO
