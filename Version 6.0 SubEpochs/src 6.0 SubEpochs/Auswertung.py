from AllResults import AllResults
from BlockParams import BlockParams
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
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

        data = {
            "FAM_A" : [],
            "FAM_B" : [],
            "FAM_C" : []
        }
        counter = {
            "FAM_A" : 0,      ##
            "FAM_B" : 0,      ##
            "FAM_C" : 0       ##
        }

        for freqCombCond in allResults:
            for famNameABC in allResults[freqCombCond]:

                for peak in allResults[freqCombCond][famNameABC]:
                    data[famNameABC].append( peak ) 
                    counter[famNameABC] +=1 


        if( info != "" and info != " " ):
            info = info + f"\n\nfamA: {counter["FAM_A"]}  famB: {counter["FAM_B"]}  famC: {counter["FAM_C"]}"    ##


        Statistics.test_sigDifference( data )
        Plots.boxplot( 
            data          = data, 
            title         = f"famA VS famB VS famC",        ##
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )


    #########################################################################################################################################################################


    @staticmethod #funzt scheinbar
    def famLMR_VS_famLMR( allResults : dict, info : str ):
        data = {
            "FAM_LEFT"   : [],
            "FAM_MIDDLE" : [],
            "FAM_RIGHT"  : []
        }
        counter = {
            "FAM_LEFT"   : [0,0,0],     ##
            "FAM_MIDDLE" : [0,0,0],     ##
            "FAM_RIGHT"  : [0,0,0]      ##
        }
        for freqCombCond in allResults:
            for famNameLMR in ["FAM_LEFT", "FAM_MIDDLE", "FAM_RIGHT"]:

                famNameABC = Konversion.get_convertedFamName(freqCombCond, famNameLMR)  ##
                for peak in allResults[freqCombCond][famNameABC]:
                    data[famNameLMR].append(peak)

                    if( famNameABC == "FAM_A" ):
                        counter[famNameLMR][0] +=1
                    elif( famNameABC == "FAM_B" ):
                        counter[famNameLMR][1] +=1
                    elif( famNameABC == "FAM_C" ):
                        counter[famNameLMR][2] +=1

        for famNameLMR in counter:                                                                     ## 
            n_peaks = counter[famNameLMR][0] + counter[famNameLMR][1] + counter[famNameLMR][2]         ## 
            for j in range( 3 ):                                                                       ##
                counter[famNameLMR][j] = round( (float(counter[famNameLMR][j]) / float(n_peaks)), 2 )  ##


        if( info != "" and info != " " ):
            info = info + f"\n\nleft: {counter["FAM_LEFT"]} \nmiddle: {counter["FAM_MIDDLE"]} \nright: {counter["FAM_RIGHT"]}"      ##


        Statistics.test_sigDifference( data )
        Plots.boxplot( 
            data          = data, 
            title         = f"famLeft VS famMiddle VS famRight",    ##
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )


#########################################################################################################################################################################