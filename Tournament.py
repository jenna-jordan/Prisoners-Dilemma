import Game
import Player
import Strategy


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


# function to play tournament and generate list of all game objects
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
