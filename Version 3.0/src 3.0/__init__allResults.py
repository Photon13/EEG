from AllResults import AllResults

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'

pNr, durchgang = 2,"2"

pathAllResultsVolt  = f"data\\results\\allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORPURPLE + "allResultsVolt" + COLOREND)
AllResults.showAllResults( pathAllResultsVolt )


pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORGREEN + "allResultsPSD" + COLOREND)
AllResults.showAllResults( pathAllResultsPSD )