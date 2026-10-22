import numpy as np
import matplotlib.pyplot as plt

ScoringList = []
ScoringList.append(np.array(
    [ 1,  2,  3,  2,  5,   # 1 to 5  # remember to subtract one from the roll to get 0-based index.  
      2,  7,  2,  9,  2,   # 6 to 10 # That's what I would have gotten from the dictionary.
     11,  2, 13,  2,  3,   # 11 to 15
      1, 17,  2, 19,  2])) # 15 to 20
DieCostList = [0, 1, 3]

nGames = 30 # keep this small enough to see individual games
nTurns = 50
nDieLimits = [6,10,20] # These will be the dies players have to choose from
nPlayers = 3
RngObj = np.random.default_rng() # random number generator

GameEndScore = 50

## 
Scores = np.zeros(shape=(nTurns, nGames, nPlayers)) # initalize at starting value for players (NaN would cause issues)
GameLength = np.empty(shape=(1, nGames, nPlayers)) # when the player first gets above winning score
GameLength[:] = np.nan
i_scoreList = 0; # placeholder for now
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
    tmpAxes.append(tmpFig[i_scoreList].add_subplot(nPlayers, 1, i_player+1))
    # if i_player == 0: # for single initializations
    tmpAxes[i_player].set_title(f"Player {i_player}")
    tmpAxes[i_player].set_xlabel("Turn")
    tmpAxes[i_player].set_ylabel("Score")
    tmpAxes[i_player].grid(True, alpha=0.3)
    for i_game in range(0,nGames):
        for i_turn in range(0,nTurns): # N.b. first turn will use initialized value at end of array
            Scores[i_turn,i_game,i_player] = Scores[i_turn-1,i_game,i_player] # start with previous score
            # this will loop around on first turn
            if i_player == 0: 
                i_die = 0
            elif i_player == 1: 
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[1]:
                    i_die = 1
                else:
                    i_die = 0
            elif i_player == 2:
                if Scores[i_turn-1,i_game,i_player] >= DieCostList[2]:
                    i_die = 2
                elif Scores[i_turn-1,i_game,i_player] >= DieCostList[1]:
                    i_die = 1
                else:
                    i_die = 0
            Scores[i_turn,i_game,i_player] = Scores[i_turn,i_game,i_player] - DieCostList[i_die]
            tmpRoll = RngObj.integers(1,nDieLimits[i_die])
            tmpScore = ScoringList[i_scoreList][tmpRoll-1] # -1 so a roll of [1] looks up the [0] index
            Scores[i_turn,i_game,i_player] = tmpScore + Scores[i_turn,i_game,i_player]
            if np.isnan(GameLength[0,i_game,i_player]) and (Scores[i_turn,i_game,i_player] >= GameEndScore):
                GameLength[0,i_game,i_player] = i_turn+1 # Remember, 0-based indexing
        # End of turns
        tmpAxes[i_player].plot(Scores[:,i_game,i_player], label=f"End {GameLength[0,i_game,i_player]}")
    # end of games
    tmpAxes_cdfEnd[0].ecdf(GameLength[0,:,i_player], label=f"Player: {i_player}")
    # tmpAxes[i_player].legend()
tmpFig[0].savefig(f"GameScores.png")
tmpAxes_cdfEnd[0].legend()
tmpFig_cdfEnd[0].savefig(f"GameLengths.png")

                
            
                
    