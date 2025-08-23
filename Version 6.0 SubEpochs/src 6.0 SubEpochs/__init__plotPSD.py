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
#typ = "threeSpeakers"
typ = "blocksInOrder"

########################
close_up = True            # <---
save     = False             # <---
########################




folderName = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\bachelorThesisText\\RESULTS\\reinmüllOrdner"
if( len( os.listdir(folderName) ) > 0 ):
    print( COLORRED + "CAVE: 'reinmüllOrdner' is not empty! " + COLOREND )
    while True:
        inp = input("Continue? [yes]: ")
        if( inp.lower() == "yes" ):
            break






if( typ == "blocksInOrder" ):
    pathAllResultsPSD  = Paths.get_pathAllResultsPSD( pNr, durchgang, "threeSpeakers")
    allResultsPSD      = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

    sec = 0
    blockNr = 0
    for i in range( len( allResultsPSD[index]["blocksInOrder_psds"] ) ):
        psds  = allResultsPSD[index]["blocksInOrder_psds"][i]
        freqs = allResultsPSD[index]["blocksInOrder_psds"][i]

        recordingElectrodes = allResultsPSD[index]["recordingElectrodes"]
        referenceElectrodes = allResultsPSD[index]["referenceElectrodes"]
        Plots.plot_PSD(
            psds, 
            freqs, 
            f"block{blockNr}",
            f"start sec{sec}",
            recordingElectrodes,
            referenceElectrodes,
            folderName, 
            pNr, 
            close_up,   
            save
        )
        if( sec == 20 ):
            sec = 0
            blockNr += 1





else:    

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