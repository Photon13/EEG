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






# CHOOSE PARTICIPANT:
pNr = 4                         # <---            
durchgang = "4"                     # <---      
###########################

basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\"
pathAllResultsVolt = basisPath + f"allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl" 
pathAllResultsPSD  = basisPath + f"allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"

AllResults.create_newAllResultsList( pathAllResultsPSD )

allResultsVolt = AllResults.loadFromPickle_allResults( pathAllResultsVolt )
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )


###########                                                         
index = 0           # <--- 
###########




allResultsPSD_newEntry = copy.deepcopy( allResultsVolt[index] )




voltDict = allResultsVolt[index]["voltDict"]

psdsDict   = copy.deepcopy( BlockParams.get_musterDict() )
freqsDict  = copy.deepcopy( BlockParams.get_musterDict() )

for freqCombCond in voltDict:
    for trial in voltDict[freqCombCond]:

        voltage = voltDict[freqCombCond][trial]

        freqs, psds = scipy.signal.periodogram(
            x       = voltage,
            fs      = allResultsVolt[index]["sfreq"],
            scaling = "density" 
        )

        psdsDict[freqCombCond][trial]  = psds
        freqsDict[freqCombCond][trial] = freqs

allResultsPSD_newEntry["psdsDict"]  = psdsDict
allResultsPSD_newEntry["freqsDict"] = freqsDict




voltage_concatAllGoodBlocks = allResultsVolt[index]["voltage_concatAllGoodBlocks"]

freqs_concatAllGoodBlocks, psds_concatAllGoodBlocks = scipy.signal.periodogram(
    x       = voltage_concatAllGoodBlocks,
    fs      = allResultsVolt[index]["sfreq"],
    scaling = "density" 
)
allResultsPSD_newEntry["psds_concatAllGoodBlocks"]  = psds_concatAllGoodBlocks
allResultsPSD_newEntry["freqs_concatAllGoodBlocks"] = freqs_concatAllGoodBlocks




allResultsPSD.append( allResultsPSD_newEntry )
AllResults.saveAsPickle_allResults( allResultsPSD, pathAllResultsPSD )
