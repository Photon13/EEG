import copy
import scipy.signal

from AllResults import AllResults
from BlockParams import BlockParams

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'






identifiers = [ 
    [13, "3"],
    [4, "4"],
    [3, "3"],
    [2, "2"],
    [1, "1"],
]

###########
index = 17       # <---
###########

for idNr in range(len(identifiers)):
    pNr = identifiers[idNr][0]
    durchgang = identifiers[idNr][1] 

    basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results Epochs\\allResultsEpochs\\"
    pathAllResultsEpochsVolt = basisPath + f"allResultsEpochsVolt_participant{pNr}_mainExp{durchgang}.pkl" 
    pathAllResultsEpochsPSD  = basisPath + f"allResultsEpochsPSD_participant{pNr}_mainExp{durchgang}.pkl"

    AllResults.create_newAllResultsList( pathAllResultsEpochsPSD )

    allResultsEpochsVolt = AllResults.loadFromPickle_allResults( pathAllResultsEpochsVolt )
    allResultsEpochsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsEpochsPSD  )





    allResultsEpochsPSD_newEntry = copy.deepcopy( allResultsEpochsVolt[index] )

    voltDict = allResultsEpochsVolt[index]["voltDict"]

    psdsDict   = {}
    freqsDict  = {}
    poss_freqCombConds = BlockParams.get_possFreqCombConds()
    for freqCombCond in poss_freqCombConds:
        psdsDict[freqCombCond] = []
        freqsDict[freqCombCond] = []



    for freqCombCond in voltDict:
        for arr in voltDict[freqCombCond]:
            voltage = arr

            freqs, psds = scipy.signal.periodogram(
                x       = voltage,
                fs      = allResultsEpochsVolt[index]["sfreq"],
                scaling = "density" 
            )

            psdsDict[freqCombCond].append( psds )
            freqsDict[freqCombCond].append( freqs )

    allResultsEpochsPSD_newEntry["psdsDict"]  = psdsDict
    allResultsEpochsPSD_newEntry["freqsDict"] = freqsDict


    allResultsEpochsPSD.append( allResultsEpochsPSD_newEntry )
    AllResults.saveAsPickle_allResults( allResultsEpochsPSD, pathAllResultsEpochsPSD )
