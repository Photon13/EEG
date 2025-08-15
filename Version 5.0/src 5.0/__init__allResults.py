from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




pNr, durchgang = 2,"2"

basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\"


pathAllResultsVolt = basisPath + f"allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl" 
print(COLORPURPLE + "allResultsVolt" + COLOREND)
AllResults.showAllResults( pathAllResultsVolt )


pathAllResultsPSD  = basisPath + f"allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORGREEN + "allResultsPSD" + COLOREND)
AllResults.showAllResults( pathAllResultsPSD )

#allResultsPSD = AllResults.loadFromPickle_allResults( pathAllResultsPSD )
#allResultsPSD[0]["psds_concatAllGoodBlocks"] = allResultsPSD[0].pop("psds_concatAllGoodBlock")
#allResultsPSD[1]["psds_concatAllGoodBlocks"] = allResultsPSD[1].pop("psds_concatAllGoodBlock")
#AllResults.saveAsPickle_allResults( allResultsPSD, pathAllResultsPSD )
