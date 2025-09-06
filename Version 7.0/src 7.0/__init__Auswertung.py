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



identifiers = { 
    "participant13_mainExp3" : [13, "3"],  #14 VS [13,15]
    "participant4_mainExp4"  : [4, "4"],   #27 VS [13,15]
    "participant3_mainExp3"  : [3, "3"],   #20 VS [13,15]
    "participant2_mainExp2"  : [2, "2"],   #20 VS [13,15]
    "participant1_mainExp1"  : [1, "1"],   #20 VS [13,15]
}

famsToUse_dict = {
    "participant13_mainExp3" : ["FAM_B"], #alle ähnlich viel, aber FAM_B meiste
    "participant4_mainExp4"  : ["FAM_A"], #massiver Überschuss FAM_A
    "participant3_mainExp3"  : ["FAM_C"], #alle ähnlich viel, aber FAM_C höchste n peaks
    "participant2_mainExp2"  : ["FAM_C"], #alle ähnlich viel, aber FAM_C höchste n peaks
    "participant1_mainExp1"  : ["FAM_A"], #massiver Überschuss FAM_A
}



#####
pNr = 4                 # <---
durchgang = "4"
index = 0

expType : str = "threeSpeakers"        
#expType : str = "singleSpeaker"

famsToUseABC : List[str] = ["FAM_A", "FAM_B", "FAM_C"]    # <---
#famsToUseABC : List[str] = ["FAM_A"]  

includeOnlySig = False                    

verbosePlots   : bool = False
#####

pathAllResults = Paths.get_pathAllResults( pNr, durchgang, expType )
allResults     = AllResults.loadFromPickle_allResults( pathAllResults )
peaksSig_quot  = allResults[index]["peaksSig_quot"]
peaksSnS_quot  = allResults[index]["peaksSnS_quot"]
peaksInOrder   = allResults[index]["peaksInOrder"]

recordingElectrodes = allResults[index]["recordingElectrodes"]
referenceElectrodes = allResults[index]["referenceElectrodes"]

if( includeOnlySig == True ):
    peakDict = peaksSig_quot
elif( includeOnlySig == False ):
    peakDict = peaksSnS_quot


if( verbosePlots == False ):
    info = ""
else:
    info = f"\n\nparticipant{pNr}"
    info = info + f"\n{recordingElectrodes} VS {referenceElectrodes}"


#######################################################################################

#Auswertung.plot_zeitlVerlaufPeaks( peaksInOrder, famsToUseABC, expType, info )

Auswertung.famABC_VS_famABC(peakDict, info, pNr)
#Auswertung.famLMR_VS_famLMR(peakDict, info, famsToUseABC, pNr)

#Auswertung.cond_VS_cond_perfamLMR( peakDict, info, famsToUseABC, "famLeft", pNr )
#Auswertung.cond_VS_cond_perfamLMR( peakDict, info, famsToUseABC, "famMiddle", pNr )
#Auswertung.cond_VS_cond_perfamLMR( peakDict, info, famsToUseABC, "famRight", pNr )
