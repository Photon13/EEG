from AllResults import AllResults
from BlockParams import BlockParams
from F_Test import F_Test

import numpy as np
import scipy
from scipy import stats

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'









########################
pNr, durchgang = 2, "2"

index = 0 # <-----
########################

fams_ABC = BlockParams.FAMS_ABC

pathAllResultsPSD  = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )


freqCombConds = list()
for key in allResultsPSD[index]["psdsDict"]:
    freqCombConds.append(key)





##################################################################################################################################################################




for freqCombCond in freqCombConds:
    for fam in fams_ABC:

        psds  = allResultsPSD[index]["psdsDict"][freqCombCond]
        freqs = allResultsPSD[index]["freqsDict"][freqCombCond]




        ############################                    <---
        n_neighbours_perSide = 120   # ca. 0.5 Hz
        #n_neighbours_perSide = 60   # ca 0.25 Hz
        ############################

        print("\n")
        print(COLORGREEN + f"{freqCombCond} fam {fam}" + COLOREND)

        #F_Test.inspect_rangeAroundFam( "psds", fam, freqs, psds )

        i_largestVal = F_Test.get_indexLargestValue_nextFam(fam, freqs, psds)
        print(psds[i_largestVal])



        # 2 bins um i_largestVal ignorieren!
        # darüber hinaus z.B. 60 bins nachbarn einbeziehen


        psds_neighbours = F_Test.get_PSDneighbours(i_largestVal, n_ignore=2, n_includePerSide=60, freqs=freqs, psds=psds)
        print(psds_neighbours)
        print(stats.f_oneway( psds[i_largestVal], psds_neighbours))


        # zählen wie oft Ergebnis signifikant ist!


