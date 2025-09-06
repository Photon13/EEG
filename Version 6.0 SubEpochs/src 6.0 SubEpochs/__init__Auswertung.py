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
    "participant13_mainExp3" : [13, "3"],  #14 VS [13,15] -> index 0
    "participant4_mainExp4"  : [4, "4"],   #27 VS [13,15] -> index 3
    "participant3_mainExp3"  : [3, "3"],   #20 VS [13,15] -> index 1
    "participant2_mainExp2"  : [2, "2"],   #20 VS [13,15] -> index 1
    "participant1_mainExp1"  : [1, "1"],  
}

famsToUse_dict = {
    "participant13_mainExp3" : ["FAM_B"], #alle ähnlich viel, aber FAM_B meiste
    "participant4_mainExp4"  : ["FAM_A"], #massiver Überschuss FAM_A
    "participant3_mainExp3"  : ["FAM_C"], #alle ähnlich viel, aber FAM_C höchste n peaks
    "participant2_mainExp2"  : ["FAM_C"], #alle ähnlich viel, aber FAM_C höchste n peaks
    "participant1_mainExp1"  : ["FAM_A"], #massiver Überschuss FAM_A
}
indicesToUse = {
    "participant13_mainExp3" : 0,
    "participant4_mainExp4"  : 3, #27 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
    "participant3_mainExp3"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant2_mainExp2"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant1_mainExp1"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
}


#####
pNr = 2
durchgang = "2"

typ : str = "threeSpeakers"

includeOnlySig : bool = True
useAllFamsABC  : bool = True
verbosePlots   : bool = True
#####

index = indicesToUse[f"participant{pNr}_mainExp{durchgang}"]

pathAllResults_sigPeaks = Paths.get_pathAllResults_sigPeaks( pNr, durchgang, typ )
pathAllResults_snSpeaks = Paths.get_pathAllResults_snSpeaks( pNr, durchgang, typ )

allResults_sigPeaks = AllResults.loadFromPickle_allResults( pathAllResults_sigPeaks )
allResults_snSpeaks = AllResults.loadFromPickle_allResults( pathAllResults_snSpeaks )



if( includeOnlySig == True ):
    allResults = allResults_sigPeaks[index]["peakDict_sig"]
elif( includeOnlySig == False ):
    allResults = allResults_snSpeaks[index]["peakDict_snS"]

recordingElectrodes = allResults_sigPeaks[index]["recordingElectrodes"]
referenceElectrodes = allResults_sigPeaks[index]["referenceElectrodes"]


if( useAllFamsABC == True ):
    famsToUseABC = ["FAM_A", "FAM_B", "FAM_C"]
else:
    famsToUseABC = famsToUse_dict[f"participant{pNr}_mainExp{durchgang}"]


if( verbosePlots == False ):
    info = ""
else:
    info = f"\n\nparticipant{pNr}"
    info = info + f"\n(includeOnlySig {includeOnlySig})"
    info = info + f"\n{recordingElectrodes} VS {referenceElectrodes}"


#######################################################################################

#Auswertung.famABC_VS_famABC(allResults, info)
#Auswertung.famLMR_VS_famLMR(allResults, info, famsToUseABC)

Auswertung.cond_VS_cond_perfamLMR( allResults, info, famsToUseABC, "famLeft" )
Auswertung.cond_VS_cond_perfamLMR( allResults, info, famsToUseABC, "famMiddle" )
Auswertung.cond_VS_cond_perfamLMR( allResults, info, famsToUseABC, "famRight" )
