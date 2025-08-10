from Target_VS_NonTarget import Target_VS_NonTarget
from BlockParams import BlockParams
from Fam_VS_Fam import Fam_VS_Fam
from AllResults import AllResults
from Statistics import Statistics
from Plots import Plots

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

from typing import List
from scipy import stats
import numpy as np
import scipy
import math
import matplotlib.pyplot as plt


COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




########################
pNr, durchgang = 2, "2"           # <---

index = 0                     # <---
########################

fams_ABC = BlockParams.FAMS_ABC

pathAllResultsPSD  : str        = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD      : List[dict] = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )






psdsABC_perFreqCombCond = Fam_VS_Fam.get_psdsABC_perFreqCombCond(allResultsPSD, index)
#print(f"\n{psdsABC_perFreqCombCond}")

psdsLMR_perFreqCombCond = Target_VS_NonTarget.get_psdsLMR_perFreqCombCond(psdsABC_perFreqCombCond)
#print(f"\n{psdsLMR_perFreqCombCond}")

psdsLMR_perCond = Target_VS_NonTarget.get_psdsLMR_perCond( psdsLMR_perFreqCombCond )
#print(f"\n{psdsLMR_perCond}")

psdsTnT_perFreqCombCond = Target_VS_NonTarget.get_psdsTnT_perFreqCombCond(psdsLMR_perFreqCombCond)
#print(f"\n{psdsTnT_perFreqCombCond}")

psdsTnT_perCond = Target_VS_NonTarget.get_psdsTnT_perCond(psdsTnT_perFreqCombCond)
#print(f"\n{psdsTnT_perCond}")





#Target_VS_NonTarget.testSigDifferent_famLMR_perCond( psdsLMR_perCond )
#Target_VS_NonTarget.testSigDifferent_target_VS_nonTarget( psdsTnT_perCond )
Target_VS_NonTarget.testSigDifferent_quotient_VS_quotient( psdsTnT_perCond )





#Target_VS_NonTarget.boxplot_target_VS_nonTarget( psdsTnT_perCond, pNr )
#Target_VS_NonTarget.boxplot_quotient_VS_quotient( psdsTnT_perCond, pNr )
#Target_VS_NonTarget.boxplot_famLMR_perCond( psdsLMR_perCond, pNr)









