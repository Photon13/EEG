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
    def covert_psdsABC_to_psds_LMR( freqCombCond :str, psdsABC : List | np.ndarray | np.ndarray[np.ndarray] ) -> List[float]:

        A = psdsABC[0]
        B = psdsABC[1]
        C = psdsABC[2]

        freqComb = str( re.findall(r"[A-C]{3}", freqCombCond)[0])

        famsLMR_dict = {
            "ABC"   : [A,B,C],
            "ACB"   : [A,C,B],
            "BAC"   : [B,A,C],
            "BCA"   : [B,C,A],
            "CAB"   : [C,A,B],
            "CBA"   : [C,B,A]
        }
        psdsLMR : List = famsLMR_dict[freqComb] 
        return psdsLMR



    @staticmethod
    def get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond : dict ) -> dict:

        psdsLMR__perFreqCombCond = dict()
        for freqCombCond in psdsABC_perFreqCombCond:
            psdsABC = psdsABC_perFreqCombCond[freqCombCond]
            psdsLMR__perFreqCombCond[freqCombCond] = Target_VS_NonTarget.covert_psdsABC_to_psds_LMR(freqCombCond, psdsABC)

        return psdsLMR__perFreqCombCond



    @staticmethod #stimmt
    def calc_psdTarget_nonTarget( freqCombCond : str, psdsLMR : List ) -> List[float]: 

        cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0]) 

        if( cond == "left" ):
            targets    = np.array( [psdsLMR[0]] )
            nonTargets = np.array( [psdsLMR[1],psdsLMR[2]] )
        elif( cond == "middle" ):
            targets    = np.array( [psdsLMR[1]] )
            nonTargets = np.array( [psdsLMR[0],psdsLMR[2]] )
        elif( cond == "right" ):
            targets    = np.array( [psdsLMR[2]] )
            nonTargets = np.array( [psdsLMR[0],psdsLMR[1]] )
        elif( cond == "both" ):
            targets    = np.array( [psdsLMR[0],psdsLMR[2]] )
            nonTargets = np.array( [psdsLMR[1]] )

        psds_target    = float( np.mean( targets ) )
        psds_nonTarget = float( np.mean( nonTargets ) )
        quotient       = float( np.divide( psds_target, psds_nonTarget ) )
        return [psds_target, psds_nonTarget, quotient]
    


    @staticmethod
    def get_psdsTnT_perFreqCombCond( psdsLMR_perFreqCombCond : dict ) -> dict:

        psdsTnT_perFreqCombCond = dict()
        for freqCombCond in psdsLMR_perFreqCombCond:
            psds_LMR : List[float] = psdsLMR_perFreqCombCond[freqCombCond]
            psdsTnT_perFreqCombCond[freqCombCond] = list( Target_VS_NonTarget.calc_psdTarget_nonTarget(freqCombCond, psds_LMR) )

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

            psdsLMR_perCond[cond]["famLeft"].append( psdsLMR_perFreqCombCond[freqCombCond][0] )
            psdsLMR_perCond[cond]["famMiddle"].append( psdsLMR_perFreqCombCond[freqCombCond][1] )
            psdsLMR_perCond[cond]["famRight"].append( psdsLMR_perFreqCombCond[freqCombCond][2] )
        return psdsLMR_perCond




    @staticmethod
    def get_psdsTnT_perCond(psdsTnT_perFreqCombCond : dict) -> dict:

        psdsTnT_perCond = dict()
        for condition in ["left", "middle", "right", "both"]:
            psdsTnT_perCond[condition] = {
                "psd_target"    : [],
                "psd_nonTarget" : [],
                "quotient"      : []
            }

        for freqCombCond in psdsTnT_perFreqCombCond:
            cond = str( re.findall( r"(left|middle|right|both)", freqCombCond )[0] ) 

            psd_target, psd_nonTarget, quotient = psdsTnT_perFreqCombCond[freqCombCond][0], psdsTnT_perFreqCombCond[freqCombCond][1], psdsTnT_perFreqCombCond[freqCombCond][2]
            psdsTnT_perCond[cond]["psd_target"].append( psd_target ) 
            psdsTnT_perCond[cond]["psd_nonTarget"].append( psd_nonTarget )
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
                "left"   : psdsLMR_perCond["left"][fam], 
                "middle" : psdsLMR_perCond["middle"][fam],
                "right"  : psdsLMR_perCond["right"][fam],
                "both"   : psdsLMR_perCond["both"][fam]
            }
            Statistics.test_sigDifference( data, method )



    @staticmethod
    def testSigDifferent_target_VS_nonTarget( psdsTnT_perCond : dict ) -> None:
        print(COLORCYAN + "\nTest sigDiff target VS nonTarget:" + COLOREND)

        for cond in ["left", "middle", "right", "both"]:
            print(COLORGREEN + f"\n{cond}" + COLOREND)

            p_values_shapiro = []
            p_values_shapiro.append( Statistics.shapiroWilk( psdsTnT_perCond[cond]["psd_target"], "psd_target" ) )
            p_values_shapiro.append( Statistics.shapiroWilk( psdsTnT_perCond[cond]["psd_nonTarget"], "psd_nonTarget" ) )
            
            if all( p_value > 0.05 for p_value in p_values_shapiro ):
                method = "t-test"
            else:
                method = "mann-whitney-u"

            data = {
                "psd_target"    : psdsTnT_perCond[cond]["psd_target"], 
                "psd_nonTarget" : psdsTnT_perCond[cond]["psd_nonTarget"] 
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
            "left" : psdsTnT_perCond["left"]["quotient"],
            "middle" : psdsTnT_perCond["middle"]["quotient"],
            "right" : psdsTnT_perCond["right"]["quotient"],
            "both" : psdsTnT_perCond["both"]["quotient"]
        }
        Plots.boxplot( 
            data          = data, 
            title         = "Quotient", 
            participantNr = participantNr, 
            ylabel        = r"$\frac{PSD(target)}{PSD(nonTarget)}$", 
            xlabel        = r"Target", 
            axhline       = 1.0
        )

    @staticmethod
    def boxplot_target_VS_nonTarget( psdsTnT_perCond : dict, participantNr : int ):
        for cond in ["left", "middle", "right", "both"]:
            data = {
                "target"    : psdsTnT_perCond[cond]["psd_target"],
                "nonTarget" : psdsTnT_perCond[cond]["psd_nonTarget"]
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








