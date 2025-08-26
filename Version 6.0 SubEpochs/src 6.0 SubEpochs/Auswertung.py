from AllResults import AllResults
from BlockParams import BlockParams
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from HelpClass_Auswertung import HelpClass_Auswertung
from Konversion import Konversion
from Statistics import Statistics
from Plots import Plots
from Paths import Paths

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


#########################################################################################################################################################################
class Auswertung:

    @staticmethod #funzt scheinbar
    def famABC_VS_famABC( allResults : dict, info : str ):

        data    = HelpClass_Auswertung.getEmptyDict_data("famsABC")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsABC")

        for freqCombCond in allResults:
            
            for famNameABC in allResults[freqCombCond]:

                for peak in allResults[freqCombCond][famNameABC]:
                    data[famNameABC].append( peak ) 
                    counter[famNameABC] +=1 


        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )


        #Rename data keys (and thus x-axis labels):
        for letter in ["A", "B", "C"]:
            data[f"fam{letter}"] = data[f"FAM_{letter}"]
            del data[f"FAM_{letter}"]

        Plots.boxplot( 
            data          = data, 
            title         = f"famA VS famB VS famC",        ##
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")


    #########################################################################################################################################################################


    @staticmethod #funzt scheinbar
    def famLMR_VS_famLMR( allResults : dict, info : str, famsToUseABC : List[str], ):

        data = HelpClass_Auswertung.getEmptyDict_data("famsLMR")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsLMRABC")

        for freqCombCond in allResults:

            for famNameLMR in ["FAM_LEFT", "FAM_MIDDLE", "FAM_RIGHT"]:
                famNameABC = Konversion.get_convertedFamName(freqCombCond, famNameLMR)  ##
                if( famNameABC in famsToUseABC ):
                    for peak in allResults[freqCombCond][famNameABC]:
                        data[famNameLMR].append(peak)
                        counter[famNameLMR][famNameABC] +=1


        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )


        #Rename data keys (and thus x-axis labels):
        for pos in ["left", "middle", "right"]:
            data[f"fam{pos.capitalize()}\n"] = data[f"FAM_{pos.upper()}"]
            del data[f"FAM_{pos.upper()}"]

        Plots.boxplot( 
            data          = data, 
            title         = f"famLeft VS famMiddle VS famRight",    ##
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")


#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################

    @staticmethod
    def famLMR_VS_famLMR_perCond( allResults : dict, info : str, famsToUseABC : List[str], targetPos : str ):

        data    = HelpClass_Auswertung.getEmptyDict_data("famsLMR")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsLMRABC")
        
        for freqCombCond in allResults:
            cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0])

            for pos in ["left", "middle", "right"]:
                if( cond == targetPos.lower() ):
                    famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_{pos.upper()}")
                    if( famNameABC in famsToUseABC ):
                        for peak in allResults[freqCombCond][famNameABC]:
                            data[f"FAM_{pos.upper()}"].append(peak)
                            counter[f"FAM_{pos.upper()}"][famNameABC] +=1

        
        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )


        #Rename data keys (and thus x-axis labels):
        for pos in ["left", "middle", "right"]:
            if( pos == targetPos.lower() ):
                targetTyp = "target"
            else:
                targetTyp = "nonTarget"

            data[f"fam{pos.capitalize()}\n({targetTyp})"] = data[f"FAM_{pos.upper()}"]
            del data[f"FAM_{pos.upper()}"]

        Plots.boxplot( 
            data          = data, 
            title         = f"target = {targetPos}",    ##
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")

#########################################################################################################################################################################

    def cond_VS_cond_perfamLMR( allResults : dict, info : str, famsToUseABC : List[str], famLMR : str ):

        data    = HelpClass_Auswertung.getEmptyDict_data("cond")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsCondABC")

        for freqCombCond in allResults:
            cond = str( re.findall(r"(left|middle|right|both)", freqCombCond)[0] )
            pos  = str( re.findall(r"(Left|Middle|Right)", famLMR)[0] )

            famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_{pos.upper()}")
            if( famNameABC in famsToUseABC ):
                for peak in allResults[freqCombCond][famNameABC]:
                        data[cond].append(peak)
                        counter[cond][famNameABC] +=1


        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )

        Plots.boxplot( 
            data          = data, 
            title         = f"{famLMR} per Condition",    ##
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")