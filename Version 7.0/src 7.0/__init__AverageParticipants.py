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
    "participant4_mainExp4"  : [4, "4"],   #27 VS [13,15] -> index 3
    "participant3_mainExp3"  : [3, "3"],   #20 VS [13,15] -> index 1
    "participant2_mainExp2"  : [2, "2"],   #20 VS [13,15] -> index 1
    "participant1_mainExp1"  : [1, "1"],  
}

indicesToUse = {
    "participant4_mainExp4"  : 0, #27 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
    "participant3_mainExp3"  : 0, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant2_mainExp2"  : 0, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant1_mainExp1"  : 0, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
}

typ = "threeSpeakers"


allPart_peakDict_sig = {}
poss_freqCombConds = BlockParams.get_possFreqCombConds()
for freqCombCond in poss_freqCombConds:
    allPart_peakDict_sig[freqCombCond] = {
        "FAM_A" : [],
        "FAM_B" : [],
        "FAM_C" : []
    }

for id in identifiers:
    pNr = identifiers[id][0]
    durchgang = identifiers[id][1]

    index = 0

    pathAllResults = Paths.get_pathAllResults( pNr, durchgang, typ )
    allResults     = AllResults.loadFromPickle_allResults( pathAllResults )
    peaksSig_quot  = allResults[index]["peaksSig_quot"]

    for freqCombCond in peaksSig_quot:
        for famABC in peaksSig_quot[freqCombCond]:
            allPart_peakDict_sig[freqCombCond][famABC].extend( peaksSig_quot[freqCombCond][famABC] )
            #for peak in peaksSig_quot[freqCombCond][famABC]:
            #    if( peak >= 5.0 ):
            #        allPart_peakDict_sig[freqCombCond][famABC].append(peak)
            


###############
famsToUseABC = ["FAM_A", "FAM_B", "FAM_C"]
#famsToUseABC = ["FAM_A"]

verbosePlots : bool = True
###############


if( verbosePlots == False ):
    info = ""
else:
    info = "\n\nall participants \n(includeOnlySig True)"
    info += "\nIncluded participants: "
    for id in identifiers:
        info += f"p{identifiers[id][0]} "







#Auswertung.famABC_VS_famABC(allPart_peakDict_sig, info)
#Auswertung.famLMR_VS_famLMR(allPart_peakDict_sig, info, famsToUseABC)

Auswertung.cond_VS_cond_perfamLMR( allPart_peakDict_sig, info, famsToUseABC, "famLeft" )
Auswertung.cond_VS_cond_perfamLMR( allPart_peakDict_sig, info, famsToUseABC, "famMiddle" )
Auswertung.cond_VS_cond_perfamLMR( allPart_peakDict_sig, info, famsToUseABC, "famRight" )