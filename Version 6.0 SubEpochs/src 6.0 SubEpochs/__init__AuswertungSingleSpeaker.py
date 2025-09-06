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




indicesToUse = {
    "participant4_mainExp4"  : 3, #27 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
    "participant3_mainExp3"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant2_mainExp2"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_C
    "participant1_mainExp1"  : 1, #20 VS [13,15] #höchste n_sigPeaks ges; und höchste n_sigPeaks FAM_A
}



#####
pNr = 3
durchgang = "3"

indexSingleSpeaker = 0
indexThreeSpeakers = indicesToUse[f"participant{pNr}_mainExp{durchgang}"]

verbosePlots : bool = True
#####



if( verbosePlots == False ):
    info = ""
else:
    info = f"\n\nparticipant{pNr}"
    info = info + f"\n(includeOnlySig True)"



famsToUseABC = ["FAM_A"]

pathAllResultsPSD_threeSpeakers  = Paths.get_pathAllResultsPSD( pNr, durchgang, "threeSpeakers" )
allResultsPSD_threeSpeakers      = AllResults.loadFromPickle_allResults( pathAllResultsPSD_threeSpeakers )

pathAllResultsPSD_singleSpeaker  = Paths.get_pathAllResultsPSD( pNr, durchgang, "singleSpeaker" )
allResultsPSD_singleSpeaker      = AllResults.loadFromPickle_allResults( pathAllResultsPSD_singleSpeaker )


#########################################################
#########################################################

sigPeaks_threeSpeakers = {}
poss_freqCombConds = BlockParams.get_possFreqCombConds()
for freqCombCond in poss_freqCombConds:
    sigPeaks_threeSpeakers[freqCombCond] = {
        "FAM_A" : [],
        "FAM_B" : [], #redundant
        "FAM_C" : []  #redundant
    }
psdsDict  = allResultsPSD_threeSpeakers[indexThreeSpeakers]["psdsDict"]
freqsDict = allResultsPSD_threeSpeakers[indexThreeSpeakers]["freqsDict"]

for freqCombCond in psdsDict:
    for intervalNr in range( len(psdsDict[freqCombCond]) ):

        psds  = psdsDict[freqCombCond][intervalNr]
        freqs = freqsDict[freqCombCond][intervalNr]

        fam                = BlockParams.FAMS_ABC["FAM_A"]
        i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
        psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
        psd_peak           = psds[i_largestVal]
        statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

        if( 0.05 >= p_value ):
            meanPsd_noise = np.mean(psds_neighbours)
            quot = psd_peak / float(meanPsd_noise)
            sigPeaks_threeSpeakers[freqCombCond]["FAM_A"].append(quot)


###
allPeaks_target    = []
allPeaks_nonTarget = []

for freqCombCond in sigPeaks_threeSpeakers:

    peaks = sigPeaks_threeSpeakers[freqCombCond]["FAM_A"]

    freqComb = str( re.findall(r"[A-C]{3}", freqCombCond)[0])
    if( freqComb == "ABC" or freqComb == "ACB" ):
        cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0])
        if( cond == "left" ):
            allPeaks_target.extend(peaks)
        elif( cond == "middle" or cond == "right" ):
            allPeaks_nonTarget.extend(peaks)


#########################################################
#########################################################

sigPeaks_singleSpeaker = {}
for attentionType in ["max_attention", "min_attention"]:
    sigPeaks_singleSpeaker[attentionType] = {
        "FAM_A" : [],
        "FAM_B" : [], #redundant
        "FAM_C" : []  #redundant
    }
psdsDict  = allResultsPSD_singleSpeaker[indexSingleSpeaker]["psdsDict"]
freqsDict = allResultsPSD_singleSpeaker[indexSingleSpeaker]["freqsDict"]

for attentionType in psdsDict:
    for intervalNr in range( len(psdsDict[attentionType]) ):

        psds  = psdsDict[attentionType][intervalNr]
        freqs = freqsDict[attentionType][intervalNr]

        fam                = BlockParams.FAMS_ABC["FAM_A"]
        i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
        psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
        psd_peak           = psds[i_largestVal]
        statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

        if( 0.05 >= p_value ):
            meanPsd_noise = np.mean(psds_neighbours)
            quot = psd_peak / float(meanPsd_noise)
            sigPeaks_singleSpeaker[attentionType]["FAM_A"].append(quot)


###
allPeaks_maxAttention = []
allPeaks_minAttention = []

for attentionArt in sigPeaks_singleSpeaker:
    peaks = sigPeaks_singleSpeaker[attentionArt]["FAM_A"] 
    if( attentionArt == "max_attention" ):
        allPeaks_maxAttention.extend(peaks)
    elif( attentionArt == "min_attention" ):
        allPeaks_minAttention.extend(peaks)


    

    

################
data = {
    "attented(1)" : allPeaks_maxAttention,
    "not attented(1)" : allPeaks_minAttention,
    "attented(3)" : allPeaks_target,
    "not attented(3)" : allPeaks_nonTarget,
}
Statistics.test_sigDifference( data )

data = {
    "attented\nsingle speaker" : allPeaks_maxAttention,
    "not attented\nsingle speaker" : allPeaks_minAttention,
    "attented\nthree speakers" : allPeaks_target,
    "not attented\nthree speakers" : allPeaks_nonTarget,
}
Plots.boxplot( 
    data          = data, 
    title         = f"attended VS not attended\nsingle speaker VS three speakers",    ##
    ylabel        = r"$\frac{PSD Peak}{PSD Noise}$]", #d.h. geteilt durch baseline s. F-Test
    xlabel        = f"\ntyp{info}", 
    axhline       = None
)
print("\n\n\n\n\n")
###################