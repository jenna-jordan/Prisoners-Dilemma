import random
import Player


class Game:

    gameCount = 0

    def __init__(self, p1: Player, p2: Player, rounds=100, noise_growthMax=0.01, noiseMax=0.5, name: str = None):
        self.p1 = p1
        self.p2 = p2
        self.rounds = rounds
        self.noise_growthMax = noise_growthMax # must be between 0 and 1
        self.noiseMax = noiseMax # must be between 0 and 1

        # shortcut for player names & strategies
        self.p1Name = self.p1.name
        self.p2Name = self.p2.name
        self.p1Strategy = self.p1.strategy.id
        self.p2Strategy = self.p2.strategy.id

        # name the game based on participating players
        if name is None:
            self.name = "{} ({}) v. {} ({})".format(self.p1Name, self.p1Strategy, self.p2Name, self.p2Strategy)
        else:
            self.name = name

        # generate game ID
        Game.gameCount += 1
        self.id = Game.gameCount

        # keep track of real and perceived moves in the game
        self.realHistory = []
        self.p1History = []
        self.p2History = []
        self.gameHistory = []

        # keep track of scores
        self.p1Score = 0
        self.p2Score = 0

        # keep track of final noise level
        self.noise = self.set_noise()
        self.noiseHistory = []

        # payoffs
        self.payoffs = self.set_payoffs()
        self.implementNoise = self.set_mode()


    def set_noise(self, max=0.5):
        """This sets the starting noise level - a random value between 0 and the max (default .5)"""
        return random.uniform(0, max)

    def set_mode(self, mode='I'):
        """Determines whether payoffs are determined by a player's actual moves (misperception) or the moves
        possibly changed by noise (misimplementation)"""
        if mode in ['misperception', 'P', 'p']:
            return False
        elif mode in ['misimplementation', 'I', 'i']:
            return True
        else:
            raise Exception("Mode must be 'P' for 'misperception', or 'I' for 'misimplementation'.")

    def set_payoffs(self, T: int = 5, R: int = 3, P: int = 1, S: int = 0):
        """This sets the payoffs for the game, determining how many points each player gets per round."""
        assert T > R > P > S, "Payoffs must follow rule: T > R > P > S"
        assert 2*R > T + S, "Payoffs must follow rule: 2*R > T + S"
        return (T, R, P, S)

    def flip(self, play):
        """This flips the player's move from 'C' to 'D' or from 'D' to 'C', if called due to noise"""
        if play == 'C':
            return 'D'
        else:
            return 'C'

    def play_round(self):
        """This plays through one round of the game. To be called once per round."""
        # get moves, as determined by each player's strategy
        p1move = self.p1.strategy.next_move(self.p1)
        p2move = self.p2.strategy.next_move(self.p2)

        realMoves = (p1move, p2move)

        # add real moves to real history
        self.realHistory.append(realMoves)

        # account for noise

        # add current noise to noise history
        self.noiseHistory.append(self.noise)

        # generate random value for each player to be compared to the noise
        p1chance = random.random()  # a value between 0 and 1
        p2chance = random.random()  # a different value between 0 and 1

        # increase noise if defection occurred
        if realMoves is ('D', 'D'):
            noiseIncrementor = random.uniform(0, self.noise_growthMax * 2)  # more noise for more defection
        elif 'D' in realMoves:
            noiseIncrementor = random.uniform(0, self.noise_growthMax)  # if only one player defects
        else:
            noiseIncrementor = (random.uniform(0, self.noise_growthMax)) * -1  # if both cooperate, reduce noise

        # increment noise, make sure noise stays between 0 and max
        self.noise += noiseIncrementor
        if self.noise > self.noiseMax:
            self.noise = self.noiseMax
        elif self.noise < 0:
            self.noise = 0
        else:
            self.noise = self.noise

        # use noise to possibly flip moves
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

        # moves (potentially altered by noise) that will determine payoffs
        noisyMoves = (p1PerMove, p2PerMove)

        # get payoff values, either default or those specified when set_payoffs() is called
        T, R, P, S = self.payoffs

        # use game mode to determine if real moves or noisy moves are used to award payoffs
        if self.implementNoise:
            moves = noisyMoves
        else:
            moves = realMoves

        # determine payoff values, to be added to the player's real scores
        if moves == ('C', 'C'):
            p1payoff = R
            p2payoff = R
        elif moves == ('D', 'D'):
            p1payoff = P
            p2payoff = P
        elif moves == ('C', 'D'):
            p1payoff = S
            p2payoff = T
        elif moves == ('D', 'C'):
            p1payoff = T
            p2payoff = S
        else:
            raise Exception("Invalid move(s) made, choose 'C' or 'D'.")

        # increment player scores
        self.p1Score += p1payoff
        self.p2Score += p2payoff

        # send moves used to determine payoffs to game history
        self.gameHistory.append(moves)



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
        self.p1.points += self.p1Score / self.rounds
        self.p2.points += self.p2Score / self.rounds

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

