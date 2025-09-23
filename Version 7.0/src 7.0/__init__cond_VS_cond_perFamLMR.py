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
        data[f"participant{pNr}"] = {}
        for key in ["data_famLeft", "data_famMiddle", "data_famRight"]:
            data[f"participant{pNr}"][key] = {
                "left"   : [],
                "middle" : [],
                "right"  : [],
                "both"   : []
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
            famsToUse = ["FAM_A"] # <---
            peakDict = peaksSig_quot
        else:
            famsToUse = ["FAM_A", "FAM_B", "FAM_C"]
            peakDict = peaksSnS_quot


        for freqCombCond in peaksSig_quot:
            cond = str( re.findall(r"(left|middle|right|both)", freqCombCond)[0] )
    
            for famPos in ["Left", "Middle", "Right"]:
                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_{famPos.upper()}")
                if( famNameABC in famsToUse ):
                    data[f"participant{pNr}"][f"data_fam{famPos.capitalize()}"][cond].extend( peakDict[freqCombCond][famNameABC] )

    
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
            #plt.yticks(np.arange(1.0, 50.0, 5.0), fontsize=tick_fontSize)

            # ---FAM_MIDDLE AND FAM_RIGHT---:
            #plt.yticks(np.arange(1.0, 14.0, 0.5), fontsize=tick_fontSize)

            # ---ALL PEAKS FAM_LEFT---:
            #plt.yticks(np.arange(11.0, 33.0, 1.0), fontsize=tick_fontSize) #___p3___
            plt.yticks(np.arange(1.0, 23.0, 1.0), fontsize=tick_fontSize)  #___p124___

            # ---ONLY SIG (FAM_A) FAM LEFT---:
            #plt.yticks(np.arange(22.0, 43.0, 1.0), fontsize=tick_fontSize) #___p3___
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

def getData_famLMR_VS_famLMR_perCond( identifiers : dict, includeOnlySig : bool ):
 
    data = {}
    for id in identifiers:
        pNr = identifiers[id][0]
        data[f"participant{pNr}"] = {}
        for key in ["data_condLeft", "data_condMiddle", "data_condRight", "data_condBoth"]:
            data[f"participant{pNr}"][key] = {
                "famLeft"   : [],
                "famMiddle" : [],
                "famRight"  : []
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
            famsToUse = ["FAM_A"] # <---
            peakDict = peaksSig_quot
        else:
            famsToUse = ["FAM_A", "FAM_B", "FAM_C"]
            peakDict = peaksSnS_quot


        for freqCombCond in peaksSig_quot:
            cond = str( re.findall(r"(left|middle|right|both)", freqCombCond)[0] )
            for famPos in ["Left", "Middle", "Right"]:
                famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_{famPos.upper()}")
                if( famNameABC in famsToUse ):
                    data[f"participant{pNr}"][f"data_cond{cond.capitalize()}"][f"fam{famPos}"].extend( peakDict[freqCombCond][famNameABC] )

    
        ##
        for data_cond in data[f"participant{pNr}"]:
            for famLMR in data[f"participant{pNr}"][data_cond]:
                print(len(data[f"participant{pNr}"][data_cond][famLMR]))
                mean = np.nanmean( data[f"participant{pNr}"][data_cond][famLMR] )
                data[f"participant{pNr}"][data_cond][famLMR] = mean

    return data


def plot__famLMR_VS_famLMR_perCond( data : dict, identifiers : dict ):
        title_fontSize = 15
        label_fontSize = 15
        tick_fontSize = 13

        colors = {
            "participant1" : "black",
            "participant2" : "blue",
            "participant3" : "orange",
            "participant4" : "grey"
        }

        for cond in ["left", "middle", "right", "both" ]: #["famLeft", "famMiddle", "famRight" ]

            plt.figure(figsize=(5, 10))

            for id in identifiers:
                pNr = identifiers[id][0]
                color = colors[f"participant{pNr}"]

                x = []
                y = []
                for famLMR in data[f"participant{pNr}"][f"data_cond{cond.capitalize()}"]:
                    x.append( famLMR )
                    y.append( data[f"participant{pNr}"][f"data_cond{cond.capitalize()}"][famLMR] )

                plt.plot( x, y, label = f"Participant {pNr}", color = color )

            
            title = f"Condition {cond}"
            plt.title(f"\n{title}", fontsize=title_fontSize, fontweight='bold', pad=20)
            plt.xlabel(f"\nfam Position", fontsize=label_fontSize)
            plt.ylabel("Mean Relative Peak Height\n", fontsize=label_fontSize) 
            

            ax = plt.subplot(111)
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            plt.xticks(fontsize=tick_fontSize, rotation=90)


            # ---FULL VIEW (IS A BIT COMPRESSED)---:
            plt.yticks(np.arange(1.0, 42.0, 2.0), fontsize=tick_fontSize)

            plt.grid( color='grey', linestyle=':', linewidth=1) #axis = 'y',

            plt.tight_layout()
            plt.show()
            inp = input("any ")

##############################################################################################################################################################
##############################################################################################################################################################


identifiers = { 
    "participant4_mainExp4"  : [4, "4"],   #27 VS [13,15] -> index 0
    "participant3_mainExp3"  : [3, "3"],   #20 VS [13,15] -> index 0
    "participant2_mainExp2"  : [2, "2"],   #20 VS [13,15] -> index 0
    "participant1_mainExp1"  : [1, "1"],   #20 VS [13,15] -> index 0
}

##
includeOnlySig = False
##

#data = getData_cond_VS_cond_perFamLMR(identifiers, includeOnlySig)
#plot__cond_VS_cond_perFamLMR(data, identifiers)

data = getData_famLMR_VS_famLMR_perCond( identifiers, includeOnlySig )
plot__famLMR_VS_famLMR_perCond( data, identifiers )