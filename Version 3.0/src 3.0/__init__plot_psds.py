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
pNr, durchgang = 2, "2"       # <---

index = 1                   # <---
########################


pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )

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


freqCombConds = list()
for key in allResultsPSD[index]["voltDict"]:
    freqCombConds.append(key)


psdsDict  = dict()
freqsDict = dict()
for freqCombCond in freqCombConds:
    avg_pows = allResultsPSD[index]["psdsDict"][freqCombCond]
    freqs    = allResultsPSD[index]["freqsDict"][freqCombCond]
    Plots.plot_PSD(
        avg_pows, 
        freqs, 
        freqCombCond, 
        folderName, 
        pNr, 
        close_up = True,      # <---
        save = True       # <---
    ) 