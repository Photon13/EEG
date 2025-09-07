from AllResults import AllResults
from BlockParams import BlockParams
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from Auswertung import Auswertung
from Konversion import Konversion
from Statistics import Statistics
from Plots import Plots
from Paths import Paths

import matplotlib.pyplot as plt
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



def getData_cond_VS_cond_perFamLMR( identifiers : dict, includeOnlySig : bool ):
 
    data = {}
    for id in identifiers:
        pNr = identifiers[id][0]
        data[f"participant{pNr}"] = {
            "data_famLeft" : {
                "left"   : [],
                "middle" : [],
                "right"  : [],
                "both"   : []
            },
            "data_famMiddle" : {
                "left"   : [],
                "middle" : [],
                "right"  : [],
                "both"   : []
            },
            "data_famRight" : {
                "left"   : [],
                "middle" : [],
                "right"  : [],
                "both"   : []
            }
        }
    ##
    for id in identifiers:
        pNr = identifiers[id][0]
        durchgang = identifiers[id][1]

        index = 0

        pathAllResults = Paths.get_pathAllResults( pNr, durchgang, "threeSpeakers" )
        allResults     = AllResults.loadFromPickle_allResults( pathAllResults )
        peaksSig_quot  = allResults[index]["peaksSig_quot"]
        peaksSnS_quot  = allResults[index]["peaksSnS_quot"]


        ##
        if( includeOnlySig == True ): 
            #Include only data from famA if all four participants shall be analysed
            #PROBLEM: p1 und p4 haben keine daten für manche freqCombConds -> Nutzung aller drei Fams würde bei Mittelung freqCombConds wieder Daten verzerren
            
            ##
            famToUse = "FAM_C" # <---
            ##

            for freqCombCond in peaksSig_quot:
                cond = str( re.findall(r"(left|middle|right|both)", freqCombCond)[0] )
    
                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_LEFT")
                if( famNameABC == famToUse ):
                    data[f"participant{pNr}"]["data_famLeft"][cond].extend( peaksSig_quot[freqCombCond][famNameABC] )

                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_MIDDLE")
                if( famNameABC == famToUse ):
                    data[f"participant{pNr}"]["data_famMiddle"][cond].extend( peaksSig_quot[freqCombCond][famNameABC] )

                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_RIGHT")
                if( famNameABC == famToUse ):
                    data[f"participant{pNr}"]["data_famRight"][cond].extend( peaksSig_quot[freqCombCond][famNameABC] )
            
        ##
        elif( includeOnlySig == False ):
            for freqCombCond in peaksSig_quot:
                cond = str( re.findall(r"(left|middle|right|both)", freqCombCond)[0] )

                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_LEFT")
                data[f"participant{pNr}"]["data_famLeft"][cond].extend( peaksSnS_quot[freqCombCond][famNameABC] )

                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_MIDDLE")
                data[f"participant{pNr}"]["data_famMiddle"][cond].extend( peaksSnS_quot[freqCombCond][famNameABC] )

                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_RIGHT")
                data[f"participant{pNr}"]["data_famRight"][cond].extend( peaksSnS_quot[freqCombCond][famNameABC] )

        
        ##
        for data_famLMR in data[f"participant{pNr}"]:
            for cond in data[f"participant{pNr}"][data_famLMR]:
                print(len(data[f"participant{pNr}"][f"{data_famLMR}"][cond]))
                meanCond = np.nanmean( data[f"participant{pNr}"][f"{data_famLMR}"][cond] )
                data[f"participant{pNr}"][f"{data_famLMR}"][cond] = meanCond

    return data



def plot__cond_VS_cond_perFamLMR( data : dict, identifiers : dict ):
        title_fontSize = 15
        label_fontSize = 15
        tick_fontSize = 13

        colors = {
            "participant1" : "black",
            "participant2" : "blue",
            "participant3" : "orange",
            "participant4" : "grey"
        }

        for famLMR in ["famLeft", "famMiddle", "famRight" ]:

            plt.figure(figsize=(5, 10))

            for id in identifiers:
                pNr = identifiers[id][0]
                color = colors[f"participant{pNr}"]

                x = []
                y = []
                for cond in data[f"participant{pNr}"][f"data_{famLMR}"]:
                    x.append( cond )
                    y.append( data[f"participant{pNr}"][f"data_{famLMR}"][cond] )

                plt.plot( x, y, label = f"participant {pNr}", color = color )

            
            title = f"{famLMR} per Condiction"
            plt.title(f"\n{title}", fontsize=title_fontSize, fontweight='bold', pad=20)
            plt.xlabel(f"\nCondition", fontsize=label_fontSize)
            plt.ylabel("Mean Relative Peak Height\n", fontsize=label_fontSize) 
            

            ax = plt.subplot(111)
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            plt.xticks(fontsize=tick_fontSize, rotation=90)


            # ---FULL VIEW (IS A BIT COMPRESSED)---:
            plt.yticks(np.arange(1.0, 50.0, 5.0), fontsize=tick_fontSize)

            # ---FAM_MIDDLE AND FAM_RIGHT---:
            #plt.yticks(np.arange(1.0, 14.0, 0.5), fontsize=tick_fontSize)

            # ---ALL PEAKS FAM_LEFT---:
            #plt.yticks(np.arange(11.0, 33.0, 1.0), fontsize=tick_fontSize) #___p3___
            #plt.yticks(np.arange(1.0, 23.0, 1.0), fontsize=tick_fontSize)  #___p124___

            # ---ONLY SIG (FAM_A) FAM LEFT---:
            #plt.yticks(np.arange(26.0, 48.0, 1.0), fontsize=tick_fontSize) #___p3___
            #plt.yticks(np.arange(1.0, 23.0, 1.0), fontsize=tick_fontSize)  #___p124___

            # ---ONLY SIG (FAM_B OR FAM_C) FAM LEFT---:
            #plt.yticks(np.arange(20.0, 59.0, 1.0), fontsize=tick_fontSize) #___p3___
            #plt.yticks(np.arange(1.0, 39.0, 1.0), fontsize=tick_fontSize)  #___p2___
 


            plt.grid( color='grey', linestyle=':', linewidth=1) #axis = 'y',

            plt.tight_layout()
            plt.show()
            inp = input("any ")


##############################################################################################################################################################
##############################################################################################################################################################


identifiers = { 
    "participant4_mainExp4"  : [4, "4"],   #27 VS [13,15] -> index 3
    "participant3_mainExp3"  : [3, "3"],   #20 VS [13,15] -> index 1
    "participant2_mainExp2"  : [2, "2"],   #20 VS [13,15] -> index 1
    "participant1_mainExp1"  : [1, "1"],   #20 VS [13,15] -> index 1
}

##
includeOnlySig = True
##

data = getData_cond_VS_cond_perFamLMR(identifiers, includeOnlySig)

plot__cond_VS_cond_perFamLMR(data, identifiers)