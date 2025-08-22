from AllResults import AllResults
from BlockParams import BlockParams
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from Statistics import Statistics
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
pNr = 13
durchgang = "3" 

index = 3
#####

pathAllResultsSigPeaks = Paths.get_pathAllResultsSigPeaks(pNr, durchgang)
allResults = AllResults.loadFromPickle_allResults( pathAllResultsSigPeaks )

#print(allResultsSigPeaks)








def test_sigDifferenceABC( allResults : List[dict], index ):
    """ Input: allResultsSigPeaks or allResultsSnSPeaks"""
    allPeaks_famABC = {
        "FAM_A" : [],
        "FAM_B" : [],
        "FAM_C" : []
    }
    for freqCombCond in allResults[index]["psdsDict"]:
        for famName in allResults[index]["psdsDict"][freqCombCond]:
            x = allResults[index]["psdsDict"][freqCombCond][famName]
            allPeaks_famABC[famName].extend( x )


    print(allPeaks_famABC)
    print(COLORGREEN + f"FAM_A : {len(allPeaks_famABC["FAM_A"])}" + COLOREND)
    print(COLORGREEN + f"FAM_B : {len(allPeaks_famABC["FAM_B"])}" + COLOREND)
    print(COLORGREEN + f"FAM_C : {len(allPeaks_famABC["FAM_C"])}" + COLOREND)
    print("\n")

    Statistics.test_sigDifference( allPeaks_famABC )








    

