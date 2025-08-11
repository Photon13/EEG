import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()
import copy
import numpy as np
import scipy.signal
from typing import List

from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'



# PSD und Power plot (scaling = "desnity" VS "spectrum") sind beinahme identisch
# Werte bei niedrigen freqs um ca 0.5 y-Achsen Einheiten verschoben



@staticmethod
def scipyPowerSpectrum(voltage : np.ndarray, sfreq : int ):
    freqs, pows = scipy.signal.periodogram(
        x       = voltage,
        fs      = sfreq,
        nfft    = 131072,
        scaling = "density" #
    )
    return pows, freqs

@staticmethod
def calcAverage( pows : List[np.ndarray] | np.ndarray ):
    if( type(pows) == List or list ):
        pows = np.array(pows)

    if( pows.ndim == 2 ):
        # === Average PSD across channels ===
        avg_pows = pows.mean(axis=0)
    else:
        avg_pows = pows
    return avg_pows







# CHOOSE PARTICIPANT:
pNr = 2                  # <---            
durchgang = "2"          # <---      
###########################


pathAllResultsVolt = f"data\\results\\allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl"
pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"

AllResults.create_newAllResultsList( pathAllResultsPSD )

allResultsVolt = AllResults.loadFromPickle_allResults( pathAllResultsVolt )
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )


AllResults.showAllResults( allResultsVolt )                                                          # <--- 
index = 1 # index of calculation    # e.g. allResultsVolt = [ [...] [...] ] for two calculations     # <--- 




sfreq               = allResultsVolt[index]["sfreq"]
recordingElectrodes = allResultsVolt[index]["recordingElectrodes"]


freqCombConds = list()
for key in allResultsVolt[index]["voltDict"]:
    freqCombConds.append(key)
#print(freqCombConds)       # freqCombConds = ["ABC_left", "CBA_middle", ...]

psdsDict  = dict()
freqsDict = dict()
for freqCombCond in freqCombConds:
    voltages = allResultsVolt[index]["voltDict"][freqCombCond]

    # SCI-PY:
    pow_list = list()
    for ch_i in range( len(recordingElectrodes) ):
        pows, freqs  = scipyPowerSpectrum( voltages[ch_i], sfreq ) # e.g. voltages = [ [U1 U2 ... Un] [U1 U2 ... Un] ] for two recording electrodes
        print(freqs)
        pow_list.append(pows)
    avg_pows      = calcAverage( pow_list ) #does nothing if 1-dim array or list with 1 entry is given
    psdsDict[f"{freqCombCond}"]  = avg_pows
    freqsDict[f"{freqCombCond}"] = freqs


# TAKE ENTRY FROM allResultsVolt AND 'APPEND' PSDS AND FREQS:
entry = copy.deepcopy(allResultsVolt[index])
entry["psdsDict"]  = psdsDict
entry["freqsDict"] = freqsDict

allResultsPSD.append(entry)
AllResults.saveAsPickle_allResults( allResultsPSD, pathAllResultsPSD )






