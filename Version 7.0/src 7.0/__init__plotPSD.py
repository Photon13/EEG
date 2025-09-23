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
pNr, durchgang = 1, "1"       # <---

index = 0                   # <---
########################

#typ = "singleSpeaker"      # <---
typ = "threeSpeakers"

########################
close_up = True            # <---
save     = True            # <---
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
psdsInOrder = allResults[index]["psdsInOrder"]

times = []
blockStart = 0
for i in range( 72 ):
    for j in range( 1, 5+1 ):
        times.append( blockStart + j*5 )
    blockStart += 30

freqs = allResults[index]["freqsDict"]["ABC_left"][0]

for i in range( len( psdsInOrder) ):
    psds = psdsInOrder[i]
    recordingElectrodes = allResults[index]["recordingElectrodes"]
    referenceElectrodes = allResults[index]["referenceElectrodes"]
    Plots.plot_PSD(
        psds, 
        freqs, 
        "",
        times[i],
        recordingElectrodes,
        referenceElectrodes,
        folderName, 
        pNr, 
        close_up,   
        save
    )