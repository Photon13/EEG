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

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



########################
pNr, durchgang = 4, "4"     # <---

index = 0                   # <---
########################


basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\"
pathAllResultsPSD  = basisPath + f"allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

print( COLORRED + f"\nparticipant{pNr}" + COLOREND )


########################    

#Y.test_sigHigherThanNoise( allResultsPSD, index )    # <---
 
########################


"""
freqs = allResultsPSD[index]["freqsDict"]["ABC_middle"]["trial1"]
psds = allResultsPSD[index]["psdsDict"]["ABC_left"]["trial1"]

HelpClass_PeakAnalysis.inspect_rangeAroundFam( 
    whichToPrint         = "freqs", 
    n_neighbours_perSide = 60, 
    fam                  = BlockParams.FAMS_ABC["FAM_C"], 
    freqs                = freqs, 
    psds                 = psds
)
"""


########################                    # <---
#trials = ["trial0"]
trials = ["trial1", "trial2", "trial3"]       
########################


psdsABC_perFreqCombCond : dict[dict] = PeaksABC.get_psdsABC_perFreqCombCond( allResultsPSD, index, trials )
psdsABC_perCond         : dict[dict] = Y.convert_perFreqCombCond_to_perCond( psdsABC_perFreqCombCond )
allPeaksABC             : dict[List] = Y.get_allPeaks( psdsABC_perFreqCombCond )

psdsLMR_perFreqCombCond : dict[dict] = PeaksLMR.get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond )
psdsLMR_perCond         : dict[dict] = Y.convert_perFreqCombCond_to_perCond( psdsLMR_perFreqCombCond )
allPeaksLMR             : dict[List] = Y.get_allPeaks( psdsLMR_perFreqCombCond )

psdsTnT_perFreqCombCond : dict[dict] = PeaksTnT.get_psdsTnT_perFreqCombCond( psdsLMR_perFreqCombCond )
psdsTnT_perCond         : dict[dict] = Y.convert_perFreqCombCond_to_perCond( psdsTnT_perFreqCombCond )
allPeaksTnT             : dict[List] = Y.get_allPeaks( psdsTnT_perFreqCombCond )



########################                            # <---
print( COLORRED + f"\n{trials}\n" + COLOREND )

Y.test_sigDiff_betweenFams( allPeaksABC )
BoxplotPeaks.boxplot_famABC_allPeaks( allPeaksABC, pNr )

#Y.test_sigDiff_betweenFams( allPeaksLMR )
#BoxplotPeaks.boxplot_famLMR_allPeaks( allPeaksLMR, pNr )

#######

#Y.test_sigDiff_betweenConds_perFam( psdsABC_perCond )
#Y.boxplot_fam_perCond( psdsABC_perCond, pNr )

#Y.test_sigDiff_betweenConds_perFam( psdsLMR_perCond )
#Y.boxplot_fam_perCond( psdsLMR_perCond, pNr )

#######

#StatisticsPeaks.testSigDifferent_target_VS_nonTarget( psdsTnT_perCond )
#BoxplotPeaks.boxplot_target_VS_nonTarget( psdsTnT_perCond, pNr )

#StatisticsPeaks.testSigDifferent_quotient_VS_quotient( psdsTnT_perCond )
#BoxplotPeaks.boxplot_quotient_VS_quotient( psdsTnT_perCond, pNr )

######################## 
