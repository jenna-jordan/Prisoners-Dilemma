import random

import Game
import Player
import Strategy


# function to create player list out of how many times each strategy should appear
def create_playerlist(strategies: dict):
    """Create a dictionary consisting of form {playername: playerObject},
    based on dictionary of form {Strategy.strategyname: #PlayersPerStrategy}"""

    players = {}

    for strat, number in strategies.items():
        for num in range(number):
            p = Player.Player(strategy=strat)
            players[p.name] = p

    return players


# default players list for use in play_tournament(), all strategies appear once
allStrategiesOnce = {'AllC' : Player.Player(strategy=Strategy.AlwaysCooperate),
                    'AllD'  : Player.Player(strategy=Strategy.AlwaysDefect),
                    'RAND'  : Player.Player(strategy=Strategy.Random),
                    'TFT'   : Player.Player(strategy=Strategy.TitForTat),
                    'TFTT'  : Player.Player(strategy=Strategy.TitForTwoTats),
                    'TTFT'  : Player.Player(strategy=Strategy.TwoTitsForTat),
                    'FBF'   : Player.Player(strategy=Strategy.FirmButFair),
                    'STFT'  : Player.Player(strategy=Strategy.SuspiciousTitForTat),
                    'HTFT'  : Player.Player(strategy=Strategy.HardTitForTat),
                    'RTFT'  : Player.Player(strategy=Strategy.ReverseTitForTat),
                    'GRIM'  : Player.Player(strategy=Strategy.GrimTrigger),
                    'SGRIM' : Player.Player(strategy=Strategy.SoftGrudger),
                    'GRAD'  : Player.Player(strategy=Strategy.Gradual),
                    'PAV'   : Player.Player(strategy=Strategy.Pavlov),
                    'SM'    : Player.Player(strategy=Strategy.SoftMajority),
                    'HM'    : Player.Player(strategy=Strategy.HardMajority)}


# alternate players list for use in play_tournament(), all strategies appear a random # of times
allStrategiesRand = {Strategy.AlwaysCooperate: random.randint(1,11),
                     Strategy.AlwaysDefect: random.randint(1,11),
                     Strategy.Random: random.randint(1, 11),
                     Strategy.TitForTat: random.randint(1, 11),
                     Strategy.TitForTwoTats: random.randint(1, 11),
                     Strategy.TwoTitsForTat: random.randint(1, 11),
                     Strategy.FirmButFair: random.randint(1, 11),
                     Strategy.SuspiciousTitForTat: random.randint(1, 11),
                     Strategy.HardTitForTat: random.randint(1, 11),
                     Strategy.ReverseTitForTat: random.randint(1, 11),
                     Strategy.GrimTrigger: random.randint(1, 11),
                     Strategy.SoftGrudger: random.randint(1, 11),
                     Strategy.Gradual: random.randint(1, 11),
                     Strategy.Pavlov: random.randint(1, 11),
                     Strategy.SoftMajority: random.randint(1, 11),
                     Strategy.HardMajority: random.randint(1, 11)}

allStrategiesRandom = create_playerlist(allStrategiesRand)


# function to play tournament and generate list of all game objects
def play_tournament(players, numrounds=100, noisegrowth=0.01, noisemax=0.5):
    """
    Play a tournament in which each player plays a game against every other player.
    :param players: a dictionary of form {'playername': playerObject}
    :param numrounds: number of rounds played for each game
    :param noisegrowth: maximum amount noise can grow/reduce each round
    :param noisemax: maximum level of noise in game
    :return: a list of all players, each player has a dict with id and stats
    """
    games = []

    # play the tournament
    for p1 in players:

        thisplayer = players[p1]

        for p2 in players:
            if players[p2] == thisplayer:
                break
            else:
                otherplayer = players[p2]

            game = Game.Game(thisplayer, otherplayer, numrounds, noisegrowth, noisemax)
            game.play_game()
            games.append(game)

    # collect the stats on each player
    players = []
    for player in players:
        playerdict = {}
        playerdict['id'] = player.name
        playerdict['strategy'] = player.strategy.id
        playerdict['scoreAvg'] = player.points / len(games)
        playerdict['winRate'] = player.wins / len(games)
        playerdict['lossRate'] = player.losses / len(games)
        playerdict['tieRate'] = player.ties / len(games)

        players.append(playerdict)

    return players
