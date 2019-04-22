import random
import Player


class Game:

    def __init__(self, p1: Player, p2: Player, rounds: int = 100, noise: float = 0, name: str = None):
        self.p1 = p1
        self.p2 = p2
        self.rounds = rounds
        self.noise = noise

        # name the game based on participating players
        if name is None:
            self.name = "{} v. {}".format(p1.name, p2.name)
        else:
            self.name = name

        # keep track of real and perceived moves in the game
        self.realHistory = []
        self.p1History = []
        self.p2History = []
        # keep track of scores
        self.p1Score = 0
        self.p2Score = 0

        # payoffs
        self.payoffs = self.set_payoffs()

    def set_payoffs(self, T: int = 5, R: int = 3, P: int = 1, S: int = 0):
        """This sets the payoffs for the game, determining how many points each player gets per round."""
        assert T > R > P > S, "Payoffs must follow rule: T > R > P > S"
        return (T, R, P, S)

    def flip(self, play):
        """This flips the player's move from 'C' to 'D' or from 'D' to 'C', if called due to noise"""
        if play == 'C':
            return 'D'
        else:
            return 'C'

    def play_round(self):
        """This plays through one round of the game.
        To be called once per round."""
        # get moves, as determined by each player's strategy
        p1move = self.p1.strategy.next_move(self.p1.history)
        p2move = self.p2.strategy.next_move(self.p2.history)
        roundMoves = (p1move, p2move)

        # add real moves to real history
        self.realHistory.append(roundMoves)

        # get payoff values, either default or those specified when set_payoffs() is called
        T, R, P, S = self.payoffs

        # determine real payoff values, to be added to the player's real scores
        if roundMoves == ('C', 'C'):
            p1payoff = R
            p2payoff = R
        elif roundMoves == ('D', 'D'):
            p1payoff = P
            p2payoff = P
        elif roundMoves == ('C', 'D'):
            p1payoff = S
            p2payoff = T
        elif roundMoves == ('D', 'C'):
            p1payoff = T
            p2payoff = S
        else:
            print("Invalid move(s) made, choose 'C' or 'D'.")

        self.p1Score += p1payoff
        self.p2Score += p2payoff

        # account for noise, then add perceived moves to perceived history

        p1chance = random.random() # a value between 0 and 1
        p2chance = random.random() # a different value between 0 and 1

        # increase noise if defection occured
        if roundMoves is ('D', 'D'):
            noiseIncrementor = random.uniform(0, 0.2) # more noise for more defection
        elif 'D' in roundMoves:
            noiseIncrementor = random.uniform(0, 0.1) # if only one player defects
        else:
            noiseIncrementor = 0

        self.noise += noiseIncrementor

        # use noise to possibly flip moves (effects player's perceptions, not real score)
        if p1chance < self.noise:
            p1PerMove = self.flip(p1move)
        else:
            p1PerMove = p1move

        if p2chance < self.noise:
            p2PerMove = self.flip(p2move)
        else:
            p2PerMove = p2move

        p1PerRound = (p1move, p2PerMove)  # P1's perceived history of the round
        p2PerRound = (p2move, p1PerMove)  # P2's perceived history of the round

        self.p1History.append(p1PerRound)
        self.p2History.append(p2PerRound)

    def send_history(self):
        """This sends the perceived moves to each player's own known history of the game.
        To be called after each round."""
        # get last moves (just played)
        forP1 = self.p1History[-1]
        forP2 = self.p2History[-1]

        # send to players's history
        self.p1.history.append(forP1)
        self.p2.history.append(forP2)

    def play_game(self):
        """This plays through an entire game between two players, for the set number of rounds."""
        # reset player histories
        self.p1.history = []
        self.p2.history = []

        # play all rounds
        for r in range(self.rounds):
            self.play_round()
            self.send_history()

        # send players their scores
        self.p1.points += self.p1Score
        self.p2.points += self.p2Score

        # send players their win/lose/tie results
        if self.p1Score == self.p2Score:
            self.p1.ties += 1
            self.p2.ties += 1
        elif self.p1Score > self.p2Score:
            self.p1.wins += 1
            self.p2.losses += 1
        elif self.p1Score < self.p2Score:
            self.p1.losses += 1
            self.p2.wins += 1

