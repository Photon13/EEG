from AllResults import AllResults
from BlockParams import BlockParams
from F_Test import F_Test

from typing import List

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


"""
########################
pNr, durchgang = 3, "3"     # <---

index = 0                   # <---
########################

 


basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results Epochs\\allResultsEpochs\\"
pathAllResultsEpochsPSD  = basisPath + f"allResultsEpochsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsEpochsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsEpochsPSD )

print( COLORRED + f"\nparticipant{pNr}" + COLOREND )
print( COLORRED + f"\nrecording electrodes {allResultsEpochsPSD[index]["recordingElectrodes"]}" + COLOREND )
print( COLORRED + f"\nrecording electrodes {allResultsEpochsPSD[index]["referenceElectrodes"]}" + COLOREND )


########################    
F_Test.f_test( allResultsEpochsPSD, index )    # <---
########################
"""

basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results Epochs\\allResultsEpochs\\"

identifiers = [ 
    [13, "3"],
    [4, "4"],
    [3, "3"],
    [2, "2"],
    [1, "1"],
]
#####
index = 3
#####

for idNr in range(len(identifiers)):
    pNr = identifiers[idNr][0]
    durchgang = identifiers[idNr][1] 
    
    pathAllResultsEpochsPSD  = basisPath + f"allResultsEpochsPSD_participant{pNr}_mainExp{durchgang}.pkl"
    allResultsEpochsPSD = AllResults.loadFromPickle_allResults( pathAllResultsEpochsPSD )

    if( idNr == 0 ):
        print( COLORCYAN + f"\nrecording electrodes {allResultsEpochsPSD[index]["recordingElectrodes"]}" + COLOREND )
        print( COLORCYAN + f"recording electrodes {allResultsEpochsPSD[index]["referenceElectrodes"]}" + COLOREND )

    print( COLORRED + f"\n\nparticipant{pNr}" + COLOREND, end="" )
    F_Test.f_test( allResultsEpochsPSD, index )

