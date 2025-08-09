from AllResults import AllResults
from BlockParams import BlockParams
from F_Test import F_Test

from scipy import stats
import numpy as np
import scipy
import math

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
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


anovaDict = F_Test.one_sidedANOVA( allResultsPSD, index, freqCombConds, fams_ABC )

for key in anovaDict:
    if( type(anovaDict[key]) == dict):
        print(COLORGREEN + f"\n{key} :\n" + COLOREND)
        if( len( anovaDict[key] ) == 0 ):
            print(COLORCYAN + f"    None" + COLOREND)
        else:
            for key2 in anovaDict[key]:
                print(COLORCYAN + f"    {key2} :" + COLOREND)
                for key3 in anovaDict[key][key2]:
                    print(f"        {key3} Hz: {anovaDict[key][key2][key3]}")
    else:
        print(f"{key} : {anovaDict[key]}")









