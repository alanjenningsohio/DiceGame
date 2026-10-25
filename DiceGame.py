import numpy as np
import matplotlib.pyplot as plt

## Set up the scoring schemes to test
ScoringList = []

# Append individual dictionaries
# ScoringList.append(np.array( # first attempt (inspired by least factor)
#     [ 1,  2,  3,  2,  5,   # 1 to 5  # remember to subtract one from the roll to get 0-based index.  
#       2,  7,  2,  9,  2,   # 6 to 10 # That's what I would have gotten from the dictionary.
#      11,  2, 13,  2,  3,   # 11 to 15
#       1, 17,  2, 19,  2])) # 15 to 20

# ScoringList.append(np.array( # Massaged for better game play
#     [ 1,  2,  3,  2,  5,   # 1 to 5
#       2,  5,  8,  6, 10,   # 6 to 10
#       4,  2,  6,  2,  5,   # 11 to 15
#       9,  7,  2, 12, 15])) # 15 to 20
# ScoringList.append(np.array( # Bonus on 3's (all)
#     [ 1,  2,  6,  2,  5,   # 1 to 5
#       6,  5,  8, 12, 10,   # 6 to 10 
#       4, 12,  6,  2, 15,   # 11 to 15
#       9,  7, 18, 12, 15])) # 15 to 20
# ScoringList.append(np.array( # bonus on 2's (but not 3's)
#     [ 1,  4,  3,  4,  5,   # 1 to 5
#       2,  5, 10,  6, 10,   # 6 to 10
#       4,  2,  6, 14,  5,   # 11 to 15
#      14,  7,  2, 12, 15])) # 15 to 20

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

nDieLimits = [6,10,20] # These will be the dies players have to choose from
# nMean = [1,2,3,5,10]
nMean = [1, 3, 10] 
# Sweeping sample size is a cheap way 
# to get a feel for the central limit, how quickly are the gains of big rolls erased. 
nRolls = 101 # prime to keep sets from repeating
RngObj = np.random.default_rng() # random number generator

## Score 
## Plot the results
Scores = np.zeros(shape=(nRolls,len(nMean),len(nDieLimits),len(ScoringList)))
tmpPrintCount = 0
tmpPrintMax = 3 # Zero disables printing the Rolls --> Score check

tmpFig = []
for i_scoreList in range(0,len(ScoringList)):
    tmpFig.append(plt.figure())
    tmpAxes = []
    for i_die in range(0,len(nDieLimits)):
        tmpAxes.append(tmpFig[i_scoreList].add_subplot(1, len(nDieLimits), i_die+1))
        if i_die == 0:
            tmpAxes[i_die].set_title(f"Plot Score {i_scoreList}, Die {nDieLimits[i_die]}")
        else:
            tmpAxes[i_die].set_title(f"Die {nDieLimits[i_die]}")
        tmpAxes[i_die].set_xlabel("Mean Score")
        tmpAxes[i_die].set_ylabel("CDF")
        tmpAxes[i_die].grid(True, alpha=0.3)
    for i_die in range(0,len(nDieLimits)):
        for i_mean in range(0,len(nMean)): 
            for i_roll in range(0,nRolls):
                tmpRoll = RngObj.integers(1,nDieLimits[i_die]+1,size=(1,nMean[i_mean])) # +1 for upper limit since it is exclusive
                tmpScores = ScoringList[i_scoreList][tmpRoll-1] # -1 so a roll of [1] looks up the [0] index
                Scores[i_roll,i_mean,i_die,i_scoreList] = np.mean(tmpScores)
                if (tmpPrintCount < tmpPrintMax and i_mean>0):
                    print(tmpRoll)
                    print(tmpScores)
                    print(Scores[i_roll,i_mean,i_die,i_scoreList])
                    tmpPrintCount = tmpPrintCount + 1
                # end loop over rolls
            tmpAxes[i_die].ecdf(Scores[:,i_mean,i_die,i_scoreList], label=f"N Rolls: {nMean[i_mean]}")
            #end size of mean (number of rolls averaged)
        print(f"ScoreList: [{i_scoreList}], d{nDieLimits[i_die]}: Mean Value = {
            np.mean(Scores[:,-1,i_die,i_scoreList])}")
        tmpAxes[i_die].legend()
        # tmpFig[i_scoreList].show() # produces a warning, and doesn't look like I need it on jupyter notebook
        # end die
        tmpFig[i_scoreList].savefig(f"MeanScores_ScoreList{i_scoreList}.png")
    # end scoreList
            


