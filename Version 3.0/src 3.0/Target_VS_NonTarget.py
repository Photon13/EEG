import re
import numpy as np
from scipy import stats
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
    def get_psdsABC_perFreqCombCond(psdsABC_perFreqCombCond : dict) -> dict:

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

        psds_target    : float = np.mean( targets )
        psds_nonTarget : float = np.mean( nonTargets )
        return [psds_target, psds_nonTarget]
    


    @staticmethod
    def get_psdsTnT_perFreqCombCond(psdsLMR__perFreqCombCond : dict) -> dict:

        psdsTnT__perFreqCombCond = dict()
        for freqCombCond in psdsLMR__perFreqCombCond:
            psds_LMR = psdsLMR__perFreqCombCond[freqCombCond]
            psdsTnT__perFreqCombCond[freqCombCond] = list( Target_VS_NonTarget.calc_psdTarget_nonTarget(freqCombCond, psds_LMR) )

        return psdsTnT__perFreqCombCond
    


    @staticmethod
    def get_psdsTnT_perCond(psdsTnT_perFreqCombCond : dict) -> dict:

        psdsTnT_perCond = dict()
        for condition in ["left", "middle", "right", "both"]:
            psdsTnT_perCond[condition] = {
                "psd_target"    : [],
                "psd_nonTarget" : []
            }

        for freqCombCond in psdsTnT_perFreqCombCond:
            cond = str( re.findall( r"(left|middle|right|both)", freqCombCond )[0] ) 

            psd_target, psd_nonTarget = psdsTnT_perFreqCombCond[freqCombCond][0], psdsTnT_perFreqCombCond[freqCombCond][1]
            psdsTnT_perCond[cond]["psd_target"].append( psd_target ) 
            psdsTnT_perCond[cond]["psd_nonTarget"].append( psd_nonTarget ) 

        return psdsTnT_perCond



    @staticmethod
    def test_whether_target_nonTarget_sigDifferent( psdsTnT_perCond : dict )-> None:
        for cond in psdsTnT_perCond:
            print(COLORGREEN + f"\n{cond}" + COLOREND)

            p_values_shapiro = list()
            for psd_type in ["psd_target", "psd_nonTarget"]:
                statistic, p_value_shapiro = stats.shapiro( psdsTnT_perCond[cond][psd_type] )
                p_values_shapiro.append(p_value_shapiro)
                print(f"Shapiro-Wilk: p_value {psd_type} = {p_value_shapiro}")

            psd_target, psd_nonTarget = psdsTnT_perCond[cond]["psd_target"], psdsTnT_perCond[cond]["psd_nonTarget"]

            if all( p_value > 0.05 for p_value in p_values_shapiro ):
                statistics, p_value = stats.ttest_ind( psd_target, psd_nonTarget,  equal_var=False )
                print(f"\nWelch's T-Test: target VS nonTarget: p_value = {p_value}")

            else:
                statistics, p_value = stats.mannwhitneyu( psd_target, psd_nonTarget )
                print(f"\nMann-Whitney_U: famA VS famB: p_value = {p_value}")


    @staticmethod
    def get_allPsds_targetNonTarget( psdsTnT_perFreqCombCond : dict ) -> dict:
        allPeaks = {
            "target" : [],
            "nonTarget" : [],
        }
        for freqCombCond in psdsTnT_perFreqCombCond:
            allPeaks["target"].append( psdsTnT_perFreqCombCond[freqCombCond][0] )
            allPeaks["nonTarget"].append( psdsTnT_perFreqCombCond[freqCombCond][1] )
        return allPeaks

    @staticmethod
    def boxplot_target_VS_nonTarget( psdsTnT_perCond : dict, participantNr : int):

        for cond in ["left", "middle", "right", "both"]:
            psds_target, psds_nonTarget = psdsTnT_perCond[cond]["psd_target"], psdsTnT_perCond[cond]["psd_nonTarget"]
            plt.boxplot( psds_target, psds_nonTarget )
            plt.xticks([1, 2], ["target", "non_target"])
            plt.title(f"PSD condition {cond}, participant{participantNr}", fontsize=14, fontweight='bold', pad=20 )
            plt.ylabel(r"$PSD$ [$\frac{V^{2}}{Hz}$]", fontsize=12)
            plt.show()
            inp = input("any ")