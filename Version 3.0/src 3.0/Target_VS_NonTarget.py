import re
import numpy as np
from scipy import stats
from typing import List
from itertools import combinations
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()
import copy

from Statistics import Statistics
from Plots import Plots

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




class Target_VS_NonTarget:

    @staticmethod #works
    def covert_psdsABC_to_psds_LMR( freqCombCond :str, psdsABC : dict ) -> List[float]:

        A = psdsABC["famA"]
        B = psdsABC["famB"]
        C = psdsABC["famC"]

        freqComb = str( re.findall(r"[A-C]{3}", freqCombCond)[0])

        famsLMR_dict = {
            "ABC"   : [A,B,C],
            "ACB"   : [A,C,B],
            "BAC"   : [B,A,C],
            "BCA"   : [B,C,A],
            "CAB"   : [C,A,B],
            "CBA"   : [C,B,A]
        }
        psdsLMR = {
            "famLeft"   : famsLMR_dict[freqComb][0],
            "famMiddle" : famsLMR_dict[freqComb][1],
            "famRight"  : famsLMR_dict[freqComb][2]
        }
        return psdsLMR



    @staticmethod
    def get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond : dict ) -> dict:

        psdsLMR_perFreqCombCond = dict()
        for freqCombCond in psdsABC_perFreqCombCond:
            psdsABC = {
                "famA" : psdsABC_perFreqCombCond[freqCombCond]["famA"],
                "famB" : psdsABC_perFreqCombCond[freqCombCond]["famB"],
                "famC" : psdsABC_perFreqCombCond[freqCombCond]["famC"]
            }

            psdsLMR : dict = Target_VS_NonTarget.covert_psdsABC_to_psds_LMR(freqCombCond, psdsABC)
            psdsLMR_perFreqCombCond[freqCombCond] = psdsLMR

        return psdsLMR_perFreqCombCond



    @staticmethod #stimmt
    def calc_psdTarget_nonTarget( freqCombCond : str, psdsLMR : List ) -> List[float]: 

        cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0]) 

        if( cond == "left" ):
            targets    = np.array( [psdsLMR["famLeft"]] )
            nonTargets = np.array( [psdsLMR["famMiddle"],psdsLMR["famRight"]] )
        elif( cond == "middle" ):
            targets    = np.array( [psdsLMR["famMiddle"]] )
            nonTargets = np.array( [psdsLMR["famLeft"],psdsLMR["famRight"]] )
        elif( cond == "right" ):
            targets    = np.array( [psdsLMR["famRight"]] )
            nonTargets = np.array( [psdsLMR["famLeft"],psdsLMR["famMiddle"]] )
        elif( cond == "both" ):
            targets    = np.array( [psdsLMR["famLeft"],psdsLMR["famRight"]] )
            nonTargets = np.array( [psdsLMR["famMiddle"]] )

        psds_target    = float( np.mean( targets ) )
        psds_nonTarget = float( np.mean( nonTargets ) )
        quotient       = float( np.divide( psds_target, psds_nonTarget ) )

        resultDict = {
            "psd_target"    : psds_target,
            "psd_nonTarget" : psds_nonTarget,
            "quotient"      : quotient
        }
        return resultDict
    


    @staticmethod
    def get_psdsTnT_perFreqCombCond( psdsLMR_perFreqCombCond : dict ) -> dict:

        psdsTnT_perFreqCombCond = dict()
        for freqCombCond in psdsLMR_perFreqCombCond:
            psds_LMR : dict = psdsLMR_perFreqCombCond[freqCombCond]

            psdsTnT_perFreqCombCond[freqCombCond] = Target_VS_NonTarget.calc_psdTarget_nonTarget(freqCombCond, psds_LMR)
        return psdsTnT_perFreqCombCond
    

    @staticmethod
    def get_psdsLMR_perCond( psdsLMR_perFreqCombCond : dict )-> dict:

        famLMR_dict = {
            "famLeft" : [],
            "famMiddle" : [],
            "famRight" : []
        }
        psdsLMR_perCond = {
            "left"   : copy.deepcopy(famLMR_dict),
            "middle" : copy.deepcopy(famLMR_dict),
            "right"  : copy.deepcopy(famLMR_dict),
            "both"   : copy.deepcopy(famLMR_dict)
        }
        for freqCombCond in psdsLMR_perFreqCombCond:
            cond = str( re.findall( r"(left|middle|right|both)", freqCombCond )[0] )

            psdsLMR_perCond[cond]["famLeft"].append( psdsLMR_perFreqCombCond[freqCombCond]["famLeft"] )
            psdsLMR_perCond[cond]["famMiddle"].append( psdsLMR_perFreqCombCond[freqCombCond]["famMiddle"] )
            psdsLMR_perCond[cond]["famRight"].append( psdsLMR_perFreqCombCond[freqCombCond]["famRight"] )
        return psdsLMR_perCond




    @staticmethod
    def get_psdsTnT_perCond(psdsTnT_perFreqCombCond : dict) -> dict:

        psdsTnT_perCond = dict()
        for condition in ["left", "middle", "right", "both"]:
            psdsTnT_perCond[condition] = {
                "psds_target"    : [],
                "psds_nonTarget" : [],
                "quotient"       : []
            }

        for freqCombCond in psdsTnT_perFreqCombCond:
            cond = str( re.findall( r"(left|middle|right|both)", freqCombCond )[0] ) 

            psd_target = psdsTnT_perFreqCombCond[freqCombCond]["psd_target"]
            psd_nonTarget = psdsTnT_perFreqCombCond[freqCombCond]["psd_nonTarget"]
            quotient = psdsTnT_perFreqCombCond[freqCombCond]["quotient"]

            psdsTnT_perCond[cond]["psds_target"].append( psd_target ) 
            psdsTnT_perCond[cond]["psds_nonTarget"].append( psd_nonTarget )
            psdsTnT_perCond[cond]["quotient"].append( quotient )

        return psdsTnT_perCond



    #############################################################################################################################################################

    @staticmethod
    def testSigDifferent_famLMR_perCond( psdsLMR_perCond : dict ):
        
        for fam in ["famLeft", "famMiddle", "famRight"]:
            print(COLORCYAN + f"\nTest sigDiff {fam} between conditions:" + COLOREND)

            p_values_shapiro = []
            for cond in ["left", "middle", "right", "both"]:
                p_values_shapiro.append( Statistics.shapiroWilk( psdsLMR_perCond[cond][fam], f"{fam}" ) )

                
            if all( p_value > 0.05 for p_value in p_values_shapiro ):
                method = "t-test"
            else:
                method = "mann-whitney-u"

            data = {
                "condition : \'target = left\'"   : psdsLMR_perCond["left"][fam], 
                "condition : \'target = middle\'" : psdsLMR_perCond["middle"][fam],
                "condition : \'target = right\'"  : psdsLMR_perCond["right"][fam],
                "condition : \'target = both\'"   : psdsLMR_perCond["both"][fam]
            }
            Statistics.test_sigDifference( data, method )



    @staticmethod
    def testSigDifferent_target_VS_nonTarget( psdsTnT_perCond : dict ) -> None:
        print(COLORCYAN + "\nTest sigDiff target VS nonTarget:" + COLOREND)

        for cond in ["left", "middle", "right", "both"]:
            print(COLORGREEN + f"\n{cond}" + COLOREND)

            p_values_shapiro = []
            p_values_shapiro.append( Statistics.shapiroWilk( psdsTnT_perCond[cond]["psds_target"], "psds_target" ) )
            p_values_shapiro.append( Statistics.shapiroWilk( psdsTnT_perCond[cond]["psds_nonTarget"], "psds_nonTarget" ) )
            
            if all( p_value > 0.05 for p_value in p_values_shapiro ):
                method = "t-test"
            else:
                method = "mann-whitney-u"

            data = {
                "psds_target"    : psdsTnT_perCond[cond]["psds_target"], 
                "psds_nonTarget" : psdsTnT_perCond[cond]["psds_nonTarget"] 
            }
            Statistics.test_sigDifference( data, method )



    @staticmethod
    def testSigDifferent_quotient_VS_quotient( psdsTnT_perCond : dict )-> None:
        print(COLORCYAN + "\nTest sigDiff quotient VS quotient:" + COLOREND)

        p_values_shapiro = []
        for cond in ["left", "middle", "right", "both"]:
            p_values_shapiro.append( Statistics.shapiroWilk( psdsTnT_perCond[cond]["quotient"], "quotient" ) )

        if all( p_value > 0.05 for p_value in p_values_shapiro ):
            method = "t-test"
        else:
            method = "mann-whitney-u"

        data = {
            "cond_left"   : psdsTnT_perCond["left"]["quotient"], 
            "cond_middle" : psdsTnT_perCond["middle"]["quotient"],
            "cond_right"  : psdsTnT_perCond["right"]["quotient"],
            "cond_both"   : psdsTnT_perCond["both"]["quotient"]
        }
        Statistics.test_sigDifference( data, method )

    #############################################################################################################################################################
    
    @staticmethod
    def boxplot_quotient_VS_quotient( psdsTnT_perCond : dict, participantNr : int ):
        data = {
            "left"   : psdsTnT_perCond["left"]["quotient"],
            "middle" : psdsTnT_perCond["middle"]["quotient"],
            "right"  : psdsTnT_perCond["right"]["quotient"],
            "both"   : psdsTnT_perCond["both"]["quotient"]
        }
        Plots.boxplot( 
            data          = data, 
            title         = "Quotient per condition", 
            participantNr = participantNr, 
            ylabel        = r"$\frac{PSD(target)}{PSD(nonTarget)}$", 
            xlabel        = r"condition", 
            axhline       = 1.0
        )

    @staticmethod
    def boxplot_target_VS_nonTarget( psdsTnT_perCond : dict, participantNr : int ):
        for cond in ["left", "middle", "right", "both"]:
            data = {
                "target"    : psdsTnT_perCond[cond]["psds_target"],
                "nonTarget" : psdsTnT_perCond[cond]["psds_nonTarget"]
            }
            Plots.boxplot( 
                data          = data, 
                title         = "PSD(target) VS PSD(nonTarget)", 
                participantNr = participantNr, 
                ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
                xlabel        = f"condition = {cond}", 
                axhline       = None
            )


    @staticmethod
    def boxplot_famLMR_perCond( psdsLMR_perCond : dict, participantNr : int ):
        for fam in ["famLeft", "famMiddle", "famRight"]:
            data = {
                "left"   : psdsLMR_perCond["left"][fam],
                "middle" : psdsLMR_perCond["middle"][fam],
                "right"  : psdsLMR_perCond["right"][fam],
                "both"   : psdsLMR_perCond["both"][fam]
            }
            Plots.boxplot( 
                data          = data, 
                title         = f"PSD({fam}) per condition", # ignores whether fam has been target or not => all data included
                participantNr = participantNr, 
                ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
                xlabel        = f"Condition", 
                axhline       = None
            )



       







