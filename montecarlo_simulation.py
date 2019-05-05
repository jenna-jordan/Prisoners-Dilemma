import pandas as pd
import random

from Tournament import play_tournament, create_playerlist
import Game
import Player
import Strategy

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

# tournaments
tCount = 0
AllTournamentStats = []
for t in range(10):
    tCount += 1
    tournament = play_tournament(allStrategiesOnce)

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
results.to_csv('results.csv')
