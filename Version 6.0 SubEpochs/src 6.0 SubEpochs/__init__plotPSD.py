from AllResults import AllResults
from Paths import Paths
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

#typ = "singleSpeaker"      # <---
typ = "threeSpeakers"

########################
close_up = True            # <---
save     = True             # <---
########################




folderName = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\bachelorThesisText\\RESULTS\\reinmüllOrdner"
if( save == True ):
    if( len( os.listdir(folderName) ) > 0 ):
        print( COLORRED + "CAVE: 'reinmüllOrdner' is not empty! " + COLOREND )
        while True:
            inp = input("Continue anyway? [yes]: ")
            if( inp.lower() == "yes" ):
                break

   

pathAllResultsPSD  = Paths.get_pathAllResultsPSD( pNr, durchgang, typ )            
allResultsPSD      = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

for freqCombCond in allResultsPSD[index]["psdsDict"]:
    for intervalNr in range( len(allResultsPSD[index]["psdsDict"][freqCombCond]) ):

        psds  = allResultsPSD[index]["psdsDict"][freqCombCond][intervalNr]
        freqs = allResultsPSD[index]["freqsDict"][freqCombCond][intervalNr]

        recordingElectrodes = allResultsPSD[index]["recordingElectrodes"]
        referenceElectrodes = allResultsPSD[index]["referenceElectrodes"]
        Plots.plot_PSD(
            psds, 
            freqs, 
            freqCombCond,
            intervalNr,
            recordingElectrodes,
            referenceElectrodes,
            folderName, 
            pNr, 
            close_up,   
            save
        )