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
    "participant4_mainExp4"  : 3, #27 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
    "participant3_mainExp3"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant2_mainExp2"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant1_mainExp1"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
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

    index = indicesToUse[id]

    pathAllResultsPSD = Paths.get_pathAllResultsPSD( pNr, durchgang, typ )
    allResultsPSD = AllResults.loadFromPickle_allResults( pathAllResultsPSD )
    psdsDict  = allResultsPSD[index]["psdsDict"]
    freqsDict = allResultsPSD[index]["freqsDict"]
    

    for freqCombCond in psdsDict:
        for intervalNr in range( len(psdsDict[freqCombCond]) ):

            psds  = psdsDict[freqCombCond][intervalNr]
            freqs = freqsDict[freqCombCond][intervalNr]

            for famName in BlockParams.FAMS_ABC:
                fam                = BlockParams.FAMS_ABC[famName]
                i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                psd_peak           = psds[i_largestVal]
                statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                if( 0.05 >= p_value ):
                    meanPsd_noise = np.mean(psds_neighbours)
                    quot = psd_peak / float(meanPsd_noise)
                    allPart_peakDict_sig[freqCombCond][famName].append(quot)






###############
#famsToUseABC = ["FAM_A", "FAM_B", "FAM_C"]
famsToUseABC = ["FAM_C"]

verbosePlots : bool = True
###############


allResults = allPart_peakDict_sig

if( verbosePlots == False ):
    info = ""
else:
    info = "\n\nall participants \n(includeOnlySig True)"






#Auswertung.famABC_VS_famABC(allResults, info)
Auswertung.famLMR_VS_famLMR(allResults, info, famsToUseABC)

Auswertung.cond_VS_cond_perfamLMR( allResults, info, famsToUseABC, "famLeft" )
Auswertung.cond_VS_cond_perfamLMR( allResults, info, famsToUseABC, "famMiddle" )
Auswertung.cond_VS_cond_perfamLMR( allResults, info, famsToUseABC, "famRight" )