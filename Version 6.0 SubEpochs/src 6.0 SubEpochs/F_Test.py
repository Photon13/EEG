from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from BlockParams import BlockParams


from typing import List
from scipy import stats
import numpy as np

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



class F_Test:

    def f_test_printAusgabe( allResultsEpochsPSD : List[dict], index : int ):

        print(COLORGREEN  + "\n\nF-Test:\n" + COLOREND)

        count_gesSig     = 0
        count_gesNonSig  = 0
        count_sig_fCC    = {}
        count_nonSig_fCC = {}


        for freqCombCond in allResultsEpochsPSD[index]["psdsDict"]:
            count_sig_fCC[freqCombCond]    = 0
            count_nonSig_fCC[freqCombCond] = 0

            psds_fCC  : List[np.ndarray] = allResultsEpochsPSD[index]["psdsDict"][freqCombCond]
            freqs_fCC : List[np.ndarray] = allResultsEpochsPSD[index]["freqsDict"][freqCombCond]

            for i in range( len( psds_fCC) ):
                for fam in BlockParams.FAMS_ABC_LIST:
                    i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds_fCC[i], freqs_fCC[i] )
                    psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds_fCC[i], freqs_fCC[i] )
                    psd_peak           = psds_fCC[i][i_largestVal]

                    statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                    if( 0.05 > p_value ):
                        count_sig_fCC[freqCombCond] +=1
                        count_gesSig+= 1
                    else:
                        count_nonSig_fCC[freqCombCond] +=1
                        count_gesNonSig += 1

        proportion = round( float(count_gesSig) / float(count_gesNonSig + count_gesSig), 2 )
        print(COLORPURPLE + f"proportion sig peaks {proportion}\n" + COLOREND) 
        for freqCombCond in allResultsEpochsPSD[index]["psdsDict"]:
            proportion_fCC = round( float(count_sig_fCC[freqCombCond]) / float( count_nonSig_fCC[freqCombCond] + count_sig_fCC[freqCombCond] ), 2)
            #print(COLORCYAN + f"{freqCombCond}: {proportion_fCC} " + COLOREND)




    #def f_test_validierungsAusgabe( allResultsEpochsPSD : List[dict], index : int ):