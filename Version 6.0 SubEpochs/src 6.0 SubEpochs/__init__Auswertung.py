from AllResults import AllResults
from BlockParams import BlockParams
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from Auswertung import Auswertung
from Konversion import Konversion
from Statistics import Statistics
from Plots import Plots
from Paths import Paths

from typing import List
import numpy as np
from scipy import stats
import copy
import re

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



#####
pNr = 3
durchgang = "3"
index = 1

typ = "threeSpeakers"
includeOnlySig = False

verbosePlots = True
#####

pathAllResults_sigPeaks = Paths.get_pathAllResults_sigPeaks(pNr, durchgang, typ)
pathAllResults_snSpeaks = Paths.get_pathAllResults_snSpeaks(pNr, durchgang, typ)

allResults_sigPeaks = AllResults.loadFromPickle_allResults( pathAllResults_sigPeaks )
allResults_snSpeaks = AllResults.loadFromPickle_allResults( pathAllResults_snSpeaks )


if( includeOnlySig == True ):
    allResults = allResults_sigPeaks[index]["peakDict_sig"]
elif( includeOnlySig == False ):
    allResults = allResults_snSpeaks[index]["peakDict_snS"]

recordingElectrodes = allResults_sigPeaks[index]["recordingElectrodes"]
referenceElectrodes = allResults_sigPeaks[index]["referenceElectrodes"]




if( verbosePlots == False ):
    info = ""
else:
    info = f"participant{pNr}"
    info = info + f"\n\n(includeOnlySig {includeOnlySig})"
    info = info + f"\n{recordingElectrodes} VS {referenceElectrodes}"



#######################################################################################


#Auswertung.famABC_VS_famABC(allResults, info)
Auswertung.famLMR_VS_famLMR(allResults, info)

#SCHEINEN BEIDE ZU FUNZEN