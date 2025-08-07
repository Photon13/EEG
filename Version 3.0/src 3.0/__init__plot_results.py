from typing import List
import mne
import pickle
import os
import sys

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

import numpy as np
import scipy.signal
import sys

from AllResults import AllResults

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'






@staticmethod
def plot_PSD(avg_pows, freqs, freqCombCond, folderName, pNr):
    plt.figure( figsize=(10, 5) )
    plt.plot(   freqs, avg_pows, label="", color = "black" )

    for fam in [35.9, 39.7, 43.2]:
        plt.axvline( fam, color='grey', linestyle=':', alpha=0.8, linewidth=3.0, zorder=0 ) # Vertical lines

    plt.title(f"{freqCombCond}", fontsize=14, fontweight='bold', pad=20 )
    plt.xlabel("$f$ [$Hz$]", fontsize=12)
    plt.ylabel(r"$PSD$ [$\frac{V^{2}}{Hz}$]", fontsize=12) 

    ####
    #min_f, max_f, step = 0.0, 60.0, 5.0    # <---

    min_f, max_f, step = 35.0, 45.0, 0.5
    plt.ylim( bottom = -1e-13, top = 0.2*1e-10  )
    ####

    plt.xlim( min_f, max_f )
    plt.xticks( np.arange(min_f, max_f+1, step) )


    plt.grid(True)
    plt.legend() #?
    plt.tight_layout() #?
    plt.show()

    
    fileName = folderName + f"\\psd_{freqCombCond}_participant{pNr}.png"

    plt.savefig(fname = fileName)   # <---
    #plt.show()                     
    #inp = input("any ")





# CHOOSE PARTICIPANT AND CALCULATION INDEX:
pNr = 2                         # <---            
durchgang = "2"                  # <---      



pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )

AllResults.showAllResults( allResultsPSD )         # <--- 
                                                       
index = 8 # index of calculation    # e.g. allResultsVolt = [ [...] [...] ] for two calculations     # <--- 
###########################################











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
#print(freqCombConds)       # freqCombConds = ["ABC_left", "CBA_middle", ...]



psdsDict  = dict()
freqsDict = dict()
for freqCombCond in freqCombConds:
    avg_pows = allResultsPSD[index]["psdsDict"][freqCombCond]
    freqs    = allResultsPSD[index]["freqsDict"][freqCombCond]
    plot_PSD(avg_pows, freqs, freqCombCond, folderName, pNr)