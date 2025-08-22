from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




pNr, durchgang = 3,"3"

basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\"


pathAllResultsVolt = basisPath + f"allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl" 
print(COLORPURPLE + "allResultsVolt" + COLOREND)
AllResults.showAllResults( pathAllResultsVolt )


pathAllResultsPSD  = basisPath + f"allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
print(COLORGREEN + "allResultsPSD" + COLOREND)
#AllResults.showAllResults( pathAllResultsPSD )






allResultsVolt = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

# pop = allResultsVolt[4].pop("voltage_concatAllGoodBlocks")
#allResultsVolt[0]["psds_voltage_concatAllGoodBlocks"] = pop[0]

#del allResultsVolt[4]
#print(allResultsVolt[4])
#AllResults.saveAsPickle_allResults( allResultsVolt, pathAllResultsVolt )

