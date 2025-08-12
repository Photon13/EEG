from AllResults import AllResults
from X import HelpClass_PeakAnalysis
from X import PeaksABC
from X import PeaksLMR
from X import PeaksTnT
from X import StatisticsPeaks
from X import BoxplotPeaks

from typing import List

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



########################
pNr, durchgang = 2, "2"     # <---

index = 0                   # <---
########################

pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD )



psdsABC_perFreqCombCond : dict[dict] = PeaksABC.get_psdsABC_perFreqCombCond( allResultsPSD, index )
psdsABC_perCond         : dict[dict] = PeaksABC.get_psdsABC_perCond( psdsABC_perFreqCombCond )
allPeaksABC             : dict[List] = PeaksABC.get_allPsdsABC_PerFam( psdsABC_perFreqCombCond )

print(COLORGREEN + f"{psdsABC_perFreqCombCond["ABC_left"]["famA"]}" + COLOREND)
print(COLORYELLOW + f"{psdsABC_perCond["left"]["famA"]}" + COLOREND)
print(COLORRED + f"{allPeaksABC}" + COLOREND)

psdsLMR_perFreqCombCond : dict[dict] = PeaksLMR.get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond )
psdsLMR_perCond         : dict[dict] = PeaksLMR.get_psdsLMR_perCond( psdsLMR_perFreqCombCond )
allPeaksLMR             : dict[List] = PeaksLMR.get_allPsdsLMR_PerFam( psdsLMR_perFreqCombCond )

print(COLORGREEN + f"{psdsLMR_perFreqCombCond["ABC_left"]["famLeft"]}" + COLOREND)
print(COLORYELLOW + f"{psdsLMR_perCond["left"]["famLeft"]}" + COLOREND)
print(COLORRED + f"{allPeaksLMR}" + COLOREND)

psdsTnT_perFreqCombCond : dict[dict] = PeaksTnT.get_psdsTnT_perFreqCombCond( psdsLMR_perFreqCombCond )
psdsTnT_perCond         : dict[dict] = PeaksTnT.get_psdsTnT_perCond( psdsTnT_perFreqCombCond )
allPeaksTnT             : dict[List] = PeaksTnT.get_allPsdsTnT( psdsTnT_perFreqCombCond )

print(COLORGREEN + f"{psdsTnT_perFreqCombCond["ABC_left"]["psd_target"]}" + COLOREND)
print(COLORYELLOW + f"{psdsTnT_perCond["left"]["psd_target"]}" + COLOREND)
print(COLORRED + f"{allPeaksTnT}" + COLOREND)



#StatisticsPeaks.test_famABC_sigHigher_thanNoise( allResultsPSD, index )
#StatisticsPeaks.testSigDifference_famABC_perCond( psdsABC_perCond )
#StatisticsPeaks.testSigDifference_famLMR_perCond( psdsLMR_perCond )
#
#
StatisticsPeaks.testSigDifferent_target_VS_nonTarget( psdsTnT_perCond )
#StatisticsPeaks.testSigDifferent_quotient_VS_quotient( psdsTnT_perCond )

#BoxplotPeaks.boxplot_famABC_allPeaks( allPeaksABC, pNr )
#BoxplotPeaks.boxplot_famLMR_allPeaks( allPeaksLMR, pNr )
#BoxplotPeaks.boxplot_famLMR_perCond( psdsLMR_perCond, pNr )
BoxplotPeaks.boxplot_target_VS_nonTarget( psdsTnT_perCond, pNr )
#BoxplotPeaks.boxplot_quotient_VS_quotient( psdsTnT_perCond, pNr )


