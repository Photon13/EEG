from AllResults import AllResults
from Plots import Plots

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import os

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'











########################
pNr, durchgang = 4, "4"       # <---

index = 0                   # <---
########################


pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

#AllResults.showAllResults( allResultsPSD )         # <--- 
                                                       









folderName = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\bachelorThesisText\\RESULTS\\reinmüllOrdner"
if( len( os.listdir(folderName) ) > 0 ):
    print( COLORRED + "CAVE: 'reinmüllOrdner' is not empty! " + COLOREND )
    while True:
        inp = input("Continue? [yes]: ")
        if( inp.lower() == "yes" ):
            break
    

sfreq               = allResultsPSD[index]["sfreq"]
recordingElectrodes = allResultsPSD[index]["recordingElectrodes"]


poss_freqCombConds = list()
for freqCombCond in allResultsPSD[index]["voltDict"]:
    if freqCombCond not in poss_freqCombConds:
        poss_freqCombConds.append(freqCombCond)


psdsDict  = dict()
freqsDict = dict()
for freqCombCond in poss_freqCombConds:
    for trial in allResultsPSD[index]["psdsDict"][freqCombCond]:
        avg_pows = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
        freqs    = allResultsPSD[index]["freqsDict"][freqCombCond][trial]
        Plots.plot_PSD(
            avg_pows, 
            freqs, 
            freqCombCond,
            trial,
            folderName, 
            pNr, 
            close_up = True,      # <---
            save = True       # <---
        ) 