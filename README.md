# Prisoner's Dilemma: with reactive noise
### Final project for IS590PR Spring 2019
### by Jenna Jordan

This project is a Monte Carlo analysis of the Prisoner's Dilemma, with reactive noise.

Reactive noise refers to the fact that the noise level of the game adjusts according to player's moves. If a player defects, the noise level increases. If both players defect, it potentially increases even more. If both players cooperate, the noise level decreases.

## Strategies

The following strategies are used in this simulation:

| ID    | Name                   | Description                                                                                                                                                                                                                                                                                           |
|-------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AllC  | Always Cooperate       | Cooperates on every move.                                                                                                                                                                                                                                                                             |
| AllD  | Always Defect          | Defects on every move.                                                                                                                                                                                                                                                                                |
| RAND  | Random                 | Makes a random move.                                                                                                                                                                                                                                                                                  |
| TFT   | Tit For Tat            | Cooperates on the first move, then copies the opponent’s last move.                                                                                                                                                                                                                                   |
| TFTT  | Tit for Two Tats       | Cooperates on the first move, and defects only when the opponent defects two times.                                                                                                                                                                                                                   |
| TTFT  | Two Tits for Tat       | Same as Tit for Tat except that it defects twice when the opponent defects.                                                                                                                                                                                                                           |
| FBF   | Firm But Fair          | Cooperates on the first move, and cooperates except after receiving a sucker payoff.                                                                                                                                                                                                                  |
| STFT  | Suspicious Tit For Tat | Same as TFT, except that it defects on the first move.                                                                                                                                                                                                                                                |
| HTFT  | Hard Tit For Tat       | Cooperates on the first move, and defects if the opponent has defects on any of the previous three moves, else cooperates.                                                                                                                                                                            |
| RTFT  | Reverse Tit for Tat    | It does the reverse of TFT. It defects on the first move, then plays the reverse of the opponent’s last move.                                                                                                                                                                                         |
| GRIM  | Grim Trigger           | Cooperates, until the opponent defects, and thereafter always defects.                                                                                                                                                                                                                                |
| SGRIM | Soft Grudger           | Like GRIM except that the opponent is punished with D,D,D,D,C,C.                                                                                                                                                                                                                                      |
| GRAD  | Gradual                | Cooperates on the first move, and cooperates as long as the opponent cooperates. After the first defection of the other player, it defects one time and cooperates two times; After the nth defection it reacts with n consecutive defections and then calms down its opponent with two cooperations. |
| PAV   | Pavlov                 | Cooperates on the first move. If a reward or temptation payoff is received in the last round then repeats last choice, otherwise chooses the opposite choice.                                                                                                                                         |
| SM    | Soft Majority          | Cooperates on the first move, and cooperates as long as the number of times the opponent has cooperated is greater than or equal to the number of times it has defected, else it defects.                                                                                                             |
| HM    | Hard Majority          | Defects on the first move, and defects if the number of defections of the opponentis greater than or equal to the number of times it has cooperated, else cooperates.                                                                                                                                 |

## Project Structure

These strategy descriptions can also be found in the table 'strategy_descriptions.csv'

The classes needed to run the tournament are found in the following files:

- 'Strategy.py' = all strategies as subclasses of an abstract base class Strategy
- 'Player.py' = Player class, which uses the Strategy class
- 'Game.py' = Game class, which uses the Player class

The code for running a tournament and the monte carlo version is found in 'Tournament.py'

Some initial results from the simulation are analyzed in the jupyter notebook 'analysis.ipynb'. *The analysis finds that the 'Soft Majority' strategy consistently has the most points.*

#### If you want to run your own tournament or monte carlo simulation, see the jupyter notebook 'Quick Start Guide.ipynb'
