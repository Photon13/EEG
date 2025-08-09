from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




pNr, durchgang = 2,"2"

pathAllResultsVolt  = f"data\\results\\allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORPURPLE + "allResultsVolt" + COLOREND)
AllResults.showAllResults( pathAllResultsVolt )


pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORGREEN + "allResultsPSD" + COLOREND)
AllResults.showAllResults( pathAllResultsPSD )