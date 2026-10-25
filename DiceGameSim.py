import numpy as np
import matplotlib.pyplot as plt

ScoringList = []
# ScoringList.append(np.array(
#     [ 1,  2,  3,  2,  5,   # 1 to 5  # remember to subtract one from the roll to get 0-based index.  
#       2,  7,  2,  9,  2,   # 6 to 10 # That's what I would have gotten from the dictionary.
#      11,  2, 13,  2,  3,   # 11 to 15
#       1, 17,  2, 19,  2])) # 15 to 20
# DieCostList = [0, 1, 3]

# ScoringList.append(np.array(
#     [ 1,  2,  3,  2,  5,   # 1 to 5  # remember to subtract one from the roll to get 0-based index.  
#       2,  5,  8,  6, 10,   # 6 to 10 # That's what I would have gotten from the dictionary.
#       4,  2,  6,  2,  5,   # 11 to 15
#       9,  7,  2, 12, 15])) # 15 to 20
# DieCostList = [0, 1, 2]

ScoringList.append(np.array( # designed by point allocations (i.e. cdf based)
    [ 2,  2,  3,  3,  4, 4,   # 1 to 6,    18pts, Avg: 3, small std
      1,  2,  9, 10,          # 7 to 10,  +22pts, Avg: 4, Larger std
      1,  1,  2,  3,  6,      # 11 to 15, +80pts, Avg: 6, even larger extremes
      8,  9,  1, 14, 15]))    # 15 to 20
ScoringList.append(np.array( # more even bonus (on 2's)
    [ 2,  4,  3,  5,  4, 6,   # 2,4,6
      1,  6,  9, 10,          # 8
      1,  4,  2,  6,  6,      # 12, 14
     10,  9,  1, 14, 15]))    # 16
ScoringList.append(np.array( # more extreme bonus
    [ 2,  2,  9,  3, 10, 4,   # 3, 5
      1,  2, 17, 10,          # 9
      1,  1,  2,  3,  6,      # 
      8, 19,  1, 24, 15]))    # 17, 19
DieCostList   = [0, 1, 2]
BonusCostList = [1, 2, 3]

nGames = 30 # keep this small enough to see individual games
nTurns = 50
nDieLimits = [6,10,20] # These will be the dies players have to choose from
playerNames = [
    "No Bonus, d6", # Could do stratagy as an anomous function, but not worth it for just this
    "No Bonus, d10",
    "No Bonus, d20",
    "2 Bonus, d6",
    "2 Bonus, d10",
    "2 Bonus, d20",
    "Big Bonus, d6",
    "Big Bonus, d10",
    "Big Bonus, d20",
]
nPlayers = len(playerNames)
RngObj = np.random.default_rng() # random number generator

GameEndScore = 40

## 
Scores = np.zeros(shape=(nTurns, nGames, nPlayers)) # initalize at starting value for players (NaN would cause issues)
GameLength = np.empty(shape=(1, nGames, nPlayers)) # when the player first gets above winning score
GameLength[:] = np.nan
tmpFig = []
tmpFig_cdfEnd = []
tmpAxes = []
tmpAxes_cdfEnd = []
tmpFig.append(plt.figure())
tmpFig_cdfEnd.append(plt.figure())
tmpAxes_cdfEnd.append(tmpFig_cdfEnd[0].add_subplot(1, 1, 1))
tmpAxes_cdfEnd[0].set_title(f"CDF")
tmpAxes_cdfEnd[0].set_xlabel("Length of Game")
tmpAxes_cdfEnd[0].set_ylabel(".")
tmpAxes_cdfEnd[0].grid(True, alpha=0.3)
for i_player in range(0,nPlayers):
    tmpAxes.append(tmpFig[0].add_subplot(3, 3, i_player+1))
    # if i_player == 0: # for single initializations
    tmpAxes[i_player].set_title(playerNames[i_player])
    tmpAxes[i_player].set_xlabel("Turn")
    tmpAxes[i_player].set_ylabel("Score")
    tmpAxes[i_player].grid(True, alpha=0.3)
    for i_game in range(0,nGames):
        for i_turn in range(0,nTurns): # N.b. first turn will use initialized value at end of array
            Scores[i_turn,i_game,i_player] = Scores[i_turn-1,i_game,i_player] # start with previous score
            # this will loop around on first turn
            if i_player == 0: # no bonus, d6
                i_die = 0
                i_bonus = 0
            elif i_player == 1: # no bonus, d10
                i_bonus = 0
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[1]:
                    i_die = 1
                else:
                    i_die = 0
            elif i_player == 2: # no bonus, d20
                i_bonus = 0
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[2]:
                    i_die = 2
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1]:
                    i_die = 1
                else:
                    i_die = 0

            elif i_player == 3: # 2 bonus, d6
                i_die = 0
                if Scores[i_turn-1,i_game,i_player] >= BonusCostList[1]:
                    i_bonus = 1
                else:
                    i_bonus = 0
            elif i_player == 4: # 2 bonus, d10
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[1] + BonusCostList[1]:
                    i_die = 1
                    i_bonus = 1
                elif Scores[i_turn-1,i_game,i_player] >= BonusCostList[1]: # could do d10 + no bonus, but this feel more congruous
                    i_die = 0
                    i_bonus = 1
                else:
                    i_die = 0
                    i_bonus = 0
            elif i_player == 5: # 2 bonus, d20
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[2] + BonusCostList[1]:
                    i_die = 2
                    i_bonus = 1
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1] + BonusCostList[1]:
                    i_die = 1
                    i_bonus = 1
                elif Scores[i_turn-1,i_game,i_player] >= BonusCostList[1]:
                    i_die = 0
                    i_bonus = 1
                else:
                    i_die = 0
                    i_bonus = 0
                    
            elif i_player == 6: # big bonus, d6
                if Scores[i_turn-1,i_game,i_player] >= BonusCostList[2]:
                    i_bonus = 2
                    i_die = 0
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1]: # d10 is more like big bonus than 2-bonus
                    i_bonus = 0
                    i_die = 1 
                else:
                    i_bonus = 0
                    i_die = 0
            elif i_player == 7: # big bonus, d10
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[1] + BonusCostList[2]:
                    i_die = 1
                    i_bonus = 2
                elif Scores[i_turn-1,i_game,i_player] >= BonusCostList[2]:
                    i_die = 0
                    i_bonus = 2
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1]:
                    i_bonus = 0
                    i_die = 1 
                else:
                    i_die = 0
                    i_bonus = 0
            elif i_player == 8: # big bonus, d20
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[2] + BonusCostList[2]:
                    i_die = 2
                    i_bonus = 2
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1] + BonusCostList[2]:
                    i_die = 1
                    i_bonus = 2
                elif Scores[i_turn-1,i_game,i_player] >= BonusCostList[2]:
                    i_die = 0
                    i_bonus = 2
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1]:
                    i_bonus = 0
                    i_die = 1 
                else:
                    i_die = 0
                    i_bonus = 0
                    
            Scores[i_turn,i_game,i_player] = Scores[i_turn,i_game,i_player] - DieCostList[i_die] - BonusCostList[i_bonus]
            tmpRoll = RngObj.integers(1,nDieLimits[i_die]+1) # +1 because upper limit is exclusive (why?!?)
            tmpScore = ScoringList[i_bonus][tmpRoll-1] # -1 so a roll of [1] looks up the [0] index
            Scores[i_turn,i_game,i_player] = tmpScore + Scores[i_turn,i_game,i_player]
            if np.isnan(GameLength[0,i_game,i_player]) and (Scores[i_turn,i_game,i_player] >= GameEndScore):
                GameLength[0,i_game,i_player] = i_turn+1 # Remember, 0-based indexing
        # End of turns
        if np.isnan(GameLength[0,i_game,i_player]):
            GameLength[0,i_game,i_player] = nTurns+10 # separate from the rest of the results, but not crazy 
        tmpAxes[i_player].plot(Scores[:,i_game,i_player], label=f"End {GameLength[0,i_game,i_player]}")
    # end of games
    tmpAxes_cdfEnd[0].ecdf(GameLength[0,:,i_player], 
                           label=playerNames[i_player],
                           linewidth=((len(playerNames) - i_player)/2+1),
                           linestyle='--')
    # tmpAxes[i_player].legend()
tmpFig[0].savefig(f"GameScores.png")
tmpAxes_cdfEnd[0].legend()
tmpFig_cdfEnd[0].savefig(f"GameLengths.png")

                
            
                
    