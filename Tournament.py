import random
import pandas as pd

import Game
import Player
import Strategy


# a list of all strategies, to be used to build a player's list
allStrategies = [Strategy.AlwaysCooperate, Strategy.AlwaysDefect, Strategy.Random, Strategy.TitForTat,
                 Strategy.TitForTwoTats, Strategy.TwoTitsForTat, Strategy.FirmButFair,
                 Strategy.SuspiciousTitForTat, Strategy.HardTitForTat, Strategy.ReverseTitForTat,
                 Strategy.GrimTrigger, Strategy.SoftGrudger, Strategy.Gradual, Strategy.Pavlov,
                 Strategy.SoftMajority, Strategy.HardMajority]


# function to create player list out of how many times each strategy should appear
def create_playerlist(strategies: dict):
    """Generate a list of players based on some number of each strategy
    :param strategies: dictionary of form {Strategy.strategyname: #PlayersPerStrategy}
    :return: dictionary consisting of form {playername: playerObject}

    >>> stratlist = {Strategy.AlwaysCooperate: 2, Strategy.AlwaysDefect: 2}
    >>> playerlist = create_playerlist(stratlist)
    >>> len(playerlist)
    4
    """

    players = {}

    for strat, number in strategies.items():
        for num in range(number):
            p = Player.Player(strategy=strat)
            players[p.name] = p

    return players


# function to create player list based on list of strategies
def create_randomized_playerlist(strategies: list, min: int, max: int):
    """
    Generate a list of players given a list of strategies,
    where each strategy will occur some number of times between the min and max
    :param strategies: a list of strategies to be used
    :param min: the minimum number of times the strategy will occur in the player list
    :param max: the maximum number of times the strategy will occur in the player list
    :return: a dictionary player list that can be used by the play_tournament function
    """
    # create dictionary of form {Strategy.strategyname: #PlayersPerStrategy} from strategy list
    strategydict = {}
    for strategy in strategies:
        strategydict[strategy] = random.randint(min, max)

    # create dictionary of form {playername: playerObject} from strategy dictionary
    playerlist = create_playerlist(strategydict)

    return playerlist


# function to play tournament and generate list of all player stats for each game
def play_tournament(players, numrounds=100, noisegrowth=0.01, noisemax=0.5, mode='I'):
    """
    Play a tournament in which each player plays a game against every other player.
    :param players: a dictionary of form {'playername': playerObject}
    :param numrounds: number of rounds played for each game
    :param noisegrowth: maximum amount noise can grow/reduce each round
    :param noisemax: maximum level of noise in game
    :param mode: set mode of game to misimplementation (I) or misperception (P)
    :return: a list of all players, each player has a dict with id and stats

    >>> stratlist = {Strategy.AlwaysCooperate: 1, Strategy.AlwaysDefect: 1}
    >>> playerlist = create_playerlist(stratlist)
    >>> t = play_tournament(playerlist, noisemax=0)
    >>> len(t)
    2
    >>> p1 = t[0]
    >>> p1['strategy']
    'AllC'
    >>> p1['winRate']
    0.0
    >>> p1['scoreAvg']
    0.0
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
            game.set_mode(mode)
            game.play_game()
            games.append(game)

    numgames = len(players) - 1
    # collect the stats on each player
    allplayers = []
    for player in players.values():
        playerdict = {}
        playerdict['id'] = player.name
        playerdict['strategy'] = player.strategy.id
        playerdict['scoreAvg'] = player.points / numgames
        playerdict['winRate'] = player.wins / numgames
        playerdict['lossRate'] = player.losses / numgames
        playerdict['tieRate'] = player.ties / numgames

        allplayers.append(playerdict)

        # reset stats for each player
        player.points = 0
        player.wins = 0
        player.losses = 0
        player.ties = 0

    return allplayers


def run_MCsim(players: dict, times=1000, filename: str = None, numrounds=100, noisegrowth=0.01, noisemax=0.5, mode='I'):
    """
    run the monte carlo simulation and export the results to a csv file
    :param players: players that will be in each tournament
    :param times: how many times the tournament will be run
    :param filename: name of the csv file results will be exported to (in Results folder) - don't include '.csv'.
                     If a filename is not specified, it will return the pandas dataframe.
    :param numrounds: number of rounds played in each game
    :param noisegrowth: max noise increment
    :param noisemax: max noise per game
    :param mode: game calculates scores based on real plays (misperception, 'P') or noisy plays (misimplementation, 'I')
    """
    tCount = 0
    AllTournamentStats = []
    for t in range(times):
        tCount += 1
        tournament = play_tournament(players, numrounds, noisegrowth, noisemax, mode)

        for player in tournament:
            tstats = {}
            tstats['TournamentID'] = tCount
            tstats['PlayerID'] = player['id']
            tstats['PlayerStrategy'] = player['strategy']
            tstats['PlayerScore'] = player['scoreAvg']
            tstats['PlayerWinRate'] = player['winRate']
            tstats['PlayerLossRate'] = player['lossRate']
            tstats['PlayerTieRate'] = player['tieRate']
            AllTournamentStats.append(tstats)

    results = pd.DataFrame(AllTournamentStats)
    results = results[['TournamentID', 'PlayerID', 'PlayerStrategy', 'PlayerScore', 'PlayerWinRate', 'PlayerLossRate', 'PlayerTieRate']]

    if filename is None:
        return results
    else:
        results.to_csv('Results/' + filename + '.csv', index=False)
