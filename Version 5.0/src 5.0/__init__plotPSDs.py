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




@staticmethod
def plot_trials123( allResultsPSD, index, pNr, folderName, close_up, save ):

    for freqCombCond in allResultsPSD[index]["psdsDict"]:
        for trial in allResultsPSD[index]["psdsDict"][freqCombCond]:
            if( trial != "trial0"):
                psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
                freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]
                Plots.plot_PSD(
                    psds, 
                    freqs, 
                    freqCombCond,
                    f"({trial})",
                    folderName, 
                    pNr, 
                    close_up,   
                    save
                ) 


@staticmethod
def plot_trial0( allResultsPSD, index, pNr, folderName, close_up, save ):
    for freqCombCond in allResultsPSD[index]["psdsDict"]:
        trial = "trial0"
        psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
        freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]
        Plots.plot_PSD(
            psds, 
            freqs, 
            freqCombCond,
            "(all trials concatenated)",
            folderName, 
            pNr, 
            close_up,
            save
        ) 


@staticmethod
def plot_psdAllGoodBlocksConcat( allResultsPSD, index, pNr, folderName, close_up, save ):
    freqCombCond = "all blocks concatenated"
    psds  = allResultsPSD[index]["psds_concatAllGoodBlocks"]
    freqs = allResultsPSD[index]["freqs_concatAllGoodBlocks"]
    Plots.plot_PSD(
        psds, 
        freqs, 
        freqCombCond,
        "",
        folderName, 
        pNr, 
        close_up,
        save
    )










########################
pNr, durchgang = 1, "1"       # <---

index = 0                   # <---
########################


basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\"
pathAllResultsPSD  = basisPath + f"allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

                                                       
folderName = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\bachelorThesisText\\RESULTS\\reinmüllOrdner"
if( len( os.listdir(folderName) ) > 0 ):
    print( COLORRED + "CAVE: 'reinmüllOrdner' is not empty! " + COLOREND )
    while True:
        inp = input("Continue? [yes]: ")
        if( inp.lower() == "yes" ):
            break
    



########################
plotTypes = ["trial0", "trials123", "allBlocks_concat"]

plotType = "trials123"         # <---

close_up = True            # <---
save     = True             # <---
########################



if( plotType == "trial0" ):
    plot_trial0( allResultsPSD, index, pNr, folderName, close_up, save )
if( plotType == "trials123"):
    plot_trials123( allResultsPSD, index, pNr, folderName, close_up, save )
if( plotType == "allBlocks_concat"):
    plot_psdAllGoodBlocksConcat( allResultsPSD, index, pNr, folderName, close_up, save )




