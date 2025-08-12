from BlockParams import BlockParams
from Fam_VS_Fam import Fam_VS_Fam
from AllResults import AllResults

from typing import List
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




########################
pNr, durchgang = 2, "2"           # <---

index = 1                     # <---
########################

fams_ABC = BlockParams.FAMS_ABC

pathAllResultsPSD  : str        = f"data\\results\\allResultsPSD_participant{pNr}_mainExp{durchgang}.pkl"
allResultsPSD      : List[dict] = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )


print( Fam_VS_Fam.get_allPsdsABC_perFam(allResultsPSD, index ) ) 

#####
Fam_VS_Fam.test_whetherPeaksFamABC_sigDifferent(allResultsPSD, index)      # <----
Fam_VS_Fam.boxplot_famABC_perCond( allResultsPSD, index, pNr )                         # <----
######









