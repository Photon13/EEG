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
pNr, durchgang = 3, "3"       # <---

index = 0                   # <---
########################

#typ = "singleSpeaker"      # <---
typ = "threeSpeakers"

########################
close_up = True            # <---
save     = False             # <---
########################




folderName = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\reinmüllOrdner"
if( save == True ):
    if( len( os.listdir(folderName) ) > 0 ):
        print( COLORRED + "CAVE: 'reinmüllOrdner' is not empty! " + COLOREND )
        while True:
            inp = input("Continue anyway? [yes]: ")
            if( inp.lower() == "yes" ):
                break

   

pathAllResults  = Paths.get_pathAllResults( pNr, durchgang, typ )            
allResults      = AllResults.loadFromPickle_allResults( pathAllResults )

for freqCombCond in allResults[index]["psdsDict"]:
    for intervalNr in range( len(allResults[index]["psdsDict"][freqCombCond]) ):

        # MONKEY PATCH:    
        #freqCombCond = "ABC_both" #
        #intervalNr   = 4          #
        
        psds  = allResults[index]["psdsDict"][freqCombCond][intervalNr]
        freqs = allResults[index]["freqsDict"][freqCombCond][intervalNr]

        recordingElectrodes = allResults[index]["recordingElectrodes"]
        referenceElectrodes = allResults[index]["referenceElectrodes"]
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