from AllResults import AllResults
from Paths import Paths

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




pNr, durchgang = 4,"4"




#pathAllResultsSubEpochsVolt = Paths.get_pathAllResultsSubEpochsVolt(pNr, durchgang) 
#print(COLORPURPLE + "allResultsSubEpochsVolt" + COLOREND)
#AllResults.showAllResults( pathAllResultsSubEpochsVolt )


#pathAllResultsSubEpochsPSD  = Paths.get_pathAllResultsSubEpochsPSD(pNr, durchgang)
#print(COLORGREEN + "allResultsSubEpochsPSD" + COLOREND)
#AllResults.showAllResults( pathAllResultsSubEpochsPSD )

pathAllResultsSigPeaks = Paths.get_pathAllResultsSigPeaks(pNr, durchgang)
print(COLORYELLOW + "allResultsSigPeaks" + COLOREND)
AllResults.showAllResults( pathAllResultsSigPeaks )