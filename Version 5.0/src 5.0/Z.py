#class Z:

from AllResults import AllResults
from BlockParams import BlockParams
from X import HelpClass_PeakAnalysis
from X import PeaksABC
from X import PeaksLMR
from X import PeaksTnT
from X import StatisticsPeaks
from Plots import BoxplotPeaks
from Y import Y

from typing import List
import matplotlib.pyplot as plt
import numpy as np
import copy

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


identifiersToInclude = [
    "participant2_mainExp2",
    "participant4_mainExp4",
    "participant1_mainExp1"
]

index = 0 # FUER ALLE!

########################                    # <---
trials = ["trial0"]
#trials = ["trial1", "trial2", "trial3"]       
########################


dict_psdsTnT_perCond = {}
dict_mean_psdsTnT_perCond = {}
dict_median_psdsTnT_perCond = {}

for identifier in identifiersToInclude:

    basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\"
    pathAllResultsPSD  = basisPath + f"allResultsPSD_{identifier}.pkl"
    allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

    psdsABC_perFreqCombCond : dict[dict] = PeaksABC.get_psdsABC_perFreqCombCond( allResultsPSD, index, trials )
    psdsABC_perCond         : dict[dict] = Y.convert_perFreqCombCond_to_perCond( psdsABC_perFreqCombCond )
    allPeaksABC             : dict[List] = Y.get_allPeaks( psdsABC_perFreqCombCond )

    psdsLMR_perFreqCombCond : dict[dict] = PeaksLMR.get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond )
    psdsLMR_perCond         : dict[dict] = Y.convert_perFreqCombCond_to_perCond( psdsLMR_perFreqCombCond )
    allPeaksLMR             : dict[List] = Y.get_allPeaks( psdsLMR_perFreqCombCond )

    psdsTnT_perFreqCombCond : dict[dict] = PeaksTnT.get_psdsTnT_perFreqCombCond( psdsLMR_perFreqCombCond )
    psdsTnT_perCond         : dict[dict] = Y.convert_perFreqCombCond_to_perCond( psdsTnT_perFreqCombCond )
    allPeaksTnT             : dict[List] = Y.get_allPeaks( psdsTnT_perFreqCombCond )

    dict_psdsTnT_perCond[identifier] = psdsTnT_perCond
    dict_mean_psdsTnT_perCond[identifier] = copy.deepcopy(psdsTnT_perCond)
    dict_median_psdsTnT_perCond[identifier] = copy.deepcopy(psdsTnT_perCond)

    for cond in dict_mean_psdsTnT_perCond[identifier]:
        for typ in ["psd_target", "psd_nonTarget", "quotient"]:
            values = dict_psdsTnT_perCond[identifier][cond][typ]
            dict_mean_psdsTnT_perCond[identifier][cond][typ]   = np.mean( values ) 
            dict_median_psdsTnT_perCond[identifier][cond][typ] = np.median( values )



print(dict_mean_psdsTnT_perCond)

for cond in dict_psdsTnT_perCond[identifier]:
    y = []
    x = []
    for identifier in identifiersToInclude:

        y.append( dict_mean_psdsTnT_perCond[identifier][cond]["psd_target"] )
        x.append(1)
        y.append( dict_mean_psdsTnT_perCond[identifier][cond]["psd_nonTarget"] )
        x.append(2)
    
    x, y = np.array(x), np.array(y)
    plt.scatter(x,y)
    plt.show()
    inp=input("any ")

