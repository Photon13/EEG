from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




pNr, durchgang = 4,"4"

basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results Epochs\\allResultsEpochs\\"


#pathAllResultsEpochsVolt = basisPath + f"allResultsEpochsVolt_participant{pNr}_mainExp{durchgang}.pkl" 
#print(COLORPURPLE + "allResultsEpochsVolt" + COLOREND)
#AllResults.showAllResults( pathAllResultsEpochsVolt )


pathAllResultsEpochsPSD  = basisPath + f"allResultsEpochsPSD_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORGREEN + "allResultsEpochsPSD" + COLOREND)
AllResults.showAllResults( pathAllResultsEpochsPSD )

"""
identifiers = [ 
    [13, "3"],
    [4, "4"],
    [3, "3"],
    [2, "2"],
    [1, "1"],
]


for idNr in range(len(identifiers)):
    pNr = identifiers[idNr][0]
    durchgang = identifiers[idNr][1] 
    pathAllResultsEpochsPSD  = basisPath + f"allResultsEpochsPSD_participant{pNr}_mainExp{durchgang}.pkl"
    allResultsPSD = AllResults.loadFromPickle_allResults( pathAllResultsEpochsPSD )

    del allResultsPSD[15]
    AllResults.saveAsPickle_allResults( allResultsPSD, pathAllResultsEpochsPSD )
"""