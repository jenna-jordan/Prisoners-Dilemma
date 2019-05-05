import pandas as pd
import random

from Tournament import play_tournament, create_playerlist
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
allStrategiesRand = {Strategy.AlwaysCooperate: random.randint(2, 5),
                     Strategy.AlwaysDefect: random.randint(2, 5),
                     Strategy.Random: random.randint(2, 5),
                     Strategy.TitForTat: random.randint(2, 5),
                     Strategy.TitForTwoTats: random.randint(2, 5),
                     Strategy.TwoTitsForTat: random.randint(2, 5),
                     Strategy.FirmButFair: random.randint(2, 5),
                     Strategy.SuspiciousTitForTat: random.randint(2, 5),
                     Strategy.HardTitForTat: random.randint(2, 5),
                     Strategy.ReverseTitForTat: random.randint(2, 5),
                     Strategy.GrimTrigger: random.randint(2, 5),
                     Strategy.SoftGrudger: random.randint(2, 5),
                     Strategy.Gradual: random.randint(2, 5),
                     Strategy.Pavlov: random.randint(2, 5),
                     Strategy.SoftMajority: random.randint(2, 5),
                     Strategy.HardMajority: random.randint(2, 5)}

allStrategiesRandom = create_playerlist(allStrategiesRand)

def run_MCsim(players: dict, times=1000, filename='results', numrounds=100, noisegrowth=0.01, noisemax=0.5, mode='I'):
    """
    run the monte carlo simulation and export the results to a csv file
    :param players: players that will be in each tournament
    :param times: how many times the tournament will be run
    :param filename: name of the csv file results will be exported to - don't include '.csv'
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
    results.to_csv(filename + '.csv', index=False)

run_MCsim(allStrategiesOnce, filename='allStrategiesOnce')
run_MCsim(allStrategiesRandom, times=500, filename='allStrategiesRandom')

run_MCsim(allStrategiesOnce, mode='P', filename='allStrategiesOnce_modeP')
run_MCsim(allStrategiesRandom, mode='P', times=100, filename='allStrategiesRandom_modeP')
