import pandas as pd

import Game
import Player
import Strategy


def create_playerlist(strategies: dict):
    """Create a dictionary consisting of form {playername: playerObject},
    based on dictionary of form {Strategy.strategyname: #PlayersPerStrategy}"""

    players = {}

    for strat, number in strategies.items():
        for num in range(number):
            p = Player.Player(strategy=strat)
            players[p.name] = p

    return players


def play_tournament(players: dict):
    """
    Play a tournament in which each player plays a game against every other player.

    :param players: a dictionary of form {playername: playerObject}
    :return: a list of all game objects from the tournament
    """
    games = []

    for p1 in players:

        thisplayer = players[p1]

        for p2 in players:
            if players[p2] == thisplayer:
                break
            else:
                otherplayer = players[p2]

            game = Game.Game(thisplayer, otherplayer)
            game.play_game()
            games.append(game)

    return games



# Test code to make sure functions work

strategies1 = {Strategy.AlwaysCooperate: 2, Strategy.AlwaysDefect: 2, Strategy.TitForTat: 4}
players1 = create_playerlist(strategies1)
tournament1 = play_tournament(players1)

for game in tournament1:
    print(game.name)
    print(game.noise)
    print(game.p1Score)
    print(game.p2Score)

for player in players1:
    print(players1[player].name)
    print(players1[player].strategy.name)
    print(players1[player].points)
