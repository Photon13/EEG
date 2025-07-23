from Main_singleBlock import Main_singleBlock
from BlockParams import BlockParams
from Berechnungen import Berechnungen
from HelpMethods import HelpMethods

import scipy
import numpy as np

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'

"""
P_fX_target = []
P_fX_nontarget = []

for blockNr in range(BlockParams.N_BLOCKS):
    psds, psds_dB, psds_normiert, freqs, blockDict = Main_singleBlock.main_singleBlock( blockNr )
    f_ABC  = [BlockParams.FAM_A, BlockParams.FAM_B, BlockParams.FAM_C]
    P_fABC_normiert = Berechnungen.berechnePower_P_fABC( fABC, 1.0, freqs, psds_normiert )
    P_fLMR_normiert = Berechnungen.bestimme_P_fLMR( freqComb, P_fABC_normiert )
    
    target = blockDict[f"block{blockNr}"]["condition"]

    # for P_fMiddle:
    if( target == "middle" ):
        P_fX_target.append( P_fLMR_normiert[1] )
    elif( target == "left" or target == "right"):
        P_fX_nontarget.append( P_fLMR_normiert[1] )


# P_fLeft für cond = left
#mean1 = 1.879132234773174
arr1 = [1.8709218409956583, 1.8412909279251717, 1.8717239108117458, 1.8775725767818954, 1.9341519173513986]

# P_fLeft für cond = middle || right
#mean2 = 1.8506506899039363
arr2 = [1.692511782181838, 1.8703444879674094, 1.8265019245173904, 1.8719824479522476, 1.9002854736176775, 1.9422780231870536]

#pvalue=0.48302300996997716

"""
#############################

P_fY = []
P_fXZ = []
for blockNr in range(BlockParams.N_BLOCKS):
    print(f"blockNr = {blockNr}")
    psds, psds_dB, psds_normiert, freqs, blockDict = Main_singleBlock.main_singleBlock( blockNr )
    P_fXYZ = Berechnungen.berechnePower_P_fABC( [32.5, 33.0, 33.5], freqs, psds_normiert, border = 0.01 ) # unnormiert

    P_fY.append(P_fXYZ[1])
    P_fXZ.append(P_fXYZ[0])
    P_fXZ.append(P_fXYZ[2])

P_fY = np.array(P_fY)
P_fXZ = np.array(P_fXZ)

print(COLORYELLOW + f"P_fY = {P_fY}" + COLOREND)
print(COLORYELLOW + f"P_fXZ = {P_fXZ}" + COLOREND)
print(COLORGREEN + f"mean(P_fY) = {HelpMethods.berechneMean_Eintraege(P_fY)}" + COLOREND)
print(COLORGREEN + f"mean(P_fXZ) = {HelpMethods.berechneMean_Eintraege(P_fXZ)}" + COLOREND)


arr1 = P_fXYZ
arr2 = P_fXZ



print(scipy.stats.shapiro(arr1)) #p>0.05 data likely from normal distribution
print(scipy.stats.shapiro(arr2))

resultTtest = scipy.stats.ttest_ind(
    arr1, arr2, 
    equal_var=False, #welch's t-test
    alternative='two-sided', 
)
print(resultTtest)


result = scipy.stats.mannwhitneyu(
    arr1, arr2,  
    alternative='two-sided',  
    method='exact' 
)
print(result)











# Gleichartige Blöcke müssen noch zusammengepoolt werden
# Export P_fABC's etc. als pd.dataframe?


# FALLS freqs identisch sein sollten für alle BLöcke, dann kann man psds_normiert über Blöcke gleicher Art mitteln
# und dann im Diagramm gegen freqs abbilden

