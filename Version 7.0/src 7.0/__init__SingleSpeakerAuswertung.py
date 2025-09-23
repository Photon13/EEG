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



pNr, durchgang = 3, "3"
index = 0

includeOnlySig : bool = False

pathAllResults_threeSp = Paths.get_pathAllResults( pNr, durchgang, "threeSpeakers" )
allResults_threeSp     = AllResults.loadFromPickle_allResults( pathAllResults_threeSp )
peaksSig_quot_threeSp  = allResults_threeSp[index]["peaksSig_quot"]
peaksSnS_quot_threeSp  = allResults_threeSp[index]["peaksSnS_quot"]

pathAllResults_singleSp = Paths.get_pathAllResults( pNr, durchgang, "singleSpeaker" )
allResults_singleSp     = AllResults.loadFromPickle_allResults( pathAllResults_singleSp )
peaksSig_quot_singleSp  = allResults_singleSp[index]["peaksSig_quot"]
peaksSnS_quot_singleSp  = allResults_singleSp[index]["peaksSnS_quot"]


if( includeOnlySig == True ):
    peakDict_threeSp  = peaksSig_quot_threeSp
    peakDict_singleSp = peaksSig_quot_singleSp
    print(COLORGREEN + "\nOnlySig " + COLOREND)

elif( includeOnlySig == False ):
    peakDict_threeSp  = peaksSnS_quot_threeSp
    peakDict_singleSp = peaksSnS_quot_singleSp
    print(COLORGREEN + "\nAllPeaks " + COLOREND)

allPeaks_target       = []
allPeaks_nonTarget    = []
allPeaks_minAttention = []
allPeaks_maxAttention = []

for freqCombCond in peakDict_threeSp:
    freqComb = str(re.findall(r"[A-C]{3}", freqCombCond)[0])
    leftFam = freqComb[0]
    if( leftFam == "A" ):
        peaks_famALeft = peakDict_threeSp[freqCombCond]["FAM_A"]
        cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0])
        if( cond == "left" ):
            allPeaks_target.extend(  peaks_famALeft )
        if( cond == "middle" or cond == "right" ):
            allPeaks_nonTarget.extend(  peaks_famALeft )

allPeaks_minAttention.extend( peakDict_singleSp["min_attention"]["FAM_A"] )
allPeaks_maxAttention.extend( peakDict_singleSp["max_attention"]["FAM_A"])

print( f"n allPeaks_maxAttention: {len( allPeaks_maxAttention )}" )
print( f"n allPeaks_minAttention: {len( allPeaks_minAttention)}" )
print( f"n allPeaks_target: {len( allPeaks_target)}" )
print( f"n allPeaks_nonTarget: {len( allPeaks_nonTarget)}")

################
data = {
    "attended_singleSpeaker"     : allPeaks_maxAttention,
    "not-attended_singleSpeaker" : allPeaks_minAttention,
    "attended_threeSpeakers"     : allPeaks_target,
    "not-attended_threeSpeakers" : allPeaks_nonTarget,
}
Statistics.test_sigDifference( data )

data = {
    "attended\nsingle speaker"     : allPeaks_maxAttention,
    "not-attended\nsingle speaker" : allPeaks_minAttention,
    "attended\nthree speakers"     : allPeaks_target,
    "not-attended\nthree speakers" : allPeaks_nonTarget,
}
Plots.boxplot( 
    data          = data, 
    title         = f"FamA from Left Speaker\n\n",    ##
    ylabel        = "Relative Peak Height\n",
    xlabel        = f"\n", 
    axhline       = None
)
print("\n\n\n\n\n")
###################

        

