from F_Test import F_Test
from BlockParams import BlockParams
from Target_VS_NonTarget import Target_VS_NonTarget
from Plots import Plots

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

from itertools import combinations
from scipy import stats
from typing import List
import numpy as np
import copy
import re

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




class Fam_VS_Fam:

    @staticmethod
    def get_peakHight(psds : np.ndarray, freqs : np.ndarray, fam : float):
        return F_Test.get_peakHight( psds, freqs, fam )
    


    @staticmethod
    def get_psdsABC_perFreqCombCond(allResultsPSD : List[dict], index : int ) -> dict:
        """ Output: {'ABC_left': {'famA': [...], 'famB' : [...], 'famC' : [...]}, 'ABC_middle': {...} ... }"""
    
        psdsABC_perFreqCombCond = dict()
        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            psdsABC_perFreqCombCond[freqCombCond] = {
                "famA" : [],
                "famB" : [],
                "famC" : []
            }
        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            for trial in ["trial1", "trial2", "trial3"]:
                psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
                freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]

                fams = ["famA", "famB", "famC"]
                for i in range( len(fams) ):
                    psd_fam = Fam_VS_Fam.get_peakHight( psds, freqs, BlockParams.FAMS_ABC[i] )
                    psdsABC_perFreqCombCond[freqCombCond][fams[i]] = psd_fam

        return psdsABC_perFreqCombCond
    


    @staticmethod
    def get_psdsABC_perCond( psdsABC_perFreqCombCond : dict )-> dict:

        famABC_dict = {
            "famA" : [],
            "famB" : [],
            "famC" : []
        }
        psdsABC_perCond = {
            "left"   : copy.deepcopy(famABC_dict),
            "middle" : copy.deepcopy(famABC_dict),
            "right"  : copy.deepcopy(famABC_dict),
            "both"   : copy.deepcopy(famABC_dict)
        }
        for freqCombCond in psdsABC_perFreqCombCond:
            cond = str( re.findall( r"(left|middle|right|both)", freqCombCond )[0] )

            psdsABC_perCond[cond]["famA"].append( psdsABC_perFreqCombCond[freqCombCond]["famA"] )
            psdsABC_perCond[cond]["famB"].append( psdsABC_perFreqCombCond[freqCombCond]["famB"] )
            psdsABC_perCond[cond]["famC"].append( psdsABC_perFreqCombCond[freqCombCond]["famC"] )
        return psdsABC_perCond

#################################################################################################################################################################

    @staticmethod
    def get_allPsdsABC_PerFam( allResultsPSD : List[dict], index : int ) -> dict[List]:
        psdsABC_perFreqCombCond = Fam_VS_Fam.get_psdsABC_perFreqCombCond(allResultsPSD, index)

        allPeaks = {
            "famA" : [],
            "famB" : [],
            "famC" : []
        }
        for freqCombCond in psdsABC_perFreqCombCond:
            allPeaks["famA"].append( psdsABC_perFreqCombCond[freqCombCond]["famA"] )
            allPeaks["famB"].append( psdsABC_perFreqCombCond[freqCombCond]["famB"] )
            allPeaks["famC"].append( psdsABC_perFreqCombCond[freqCombCond]["famC"] )

        return allPeaks
    

    @staticmethod
    def get_allPsdsLMR_PerFam( allResultsPSD : List[dict], index : int ) -> dict[List]:
        psdsABC_perFreqCombCond = Fam_VS_Fam.get_psdsABC_perFreqCombCond( allResultsPSD, index )
        psdsLMR_perFreqCombCond = Target_VS_NonTarget.get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond )

        allPeaks = {
            "famLeft" : [],
            "famMiddle" : [],
            "famRight" : []
        }
        for freqCombCond in psdsABC_perFreqCombCond:
            allPeaks["famLeft"].append( psdsLMR_perFreqCombCond[freqCombCond]["famLeft"] )
            allPeaks["famMiddle"].append( psdsLMR_perFreqCombCond[freqCombCond]["famMiddle"] )
            allPeaks["famRight"].append( psdsLMR_perFreqCombCond[freqCombCond]["famRight"] )

        return allPeaks

#################################################################################################################################################################

    @staticmethod
    def test_whetherPeaksFamABC_sigDifferent(allResultsPSD : List[dict], index : int):

        allPeaks = Fam_VS_Fam.get_allPsdsABC_PerFam(allResultsPSD, index)

        p_values_shapiro = list()
        print("\n")
        for fam in allPeaks:
            statistic, p_value_shapiro = stats.shapiro( allPeaks[fam] )
            p_values_shapiro.append( p_value_shapiro )
            print(f"Shapiro-Wilk: p_value {fam} = {p_value_shapiro}")
        print("\n")

        combos = list( combinations( ["famA", "famB","famC"], 2) )
        for combo in combos:
            fam1, fam2 = combo[0], combo[1]

            if all(p_value > 0.05 for p_value in p_values_shapiro):
                statistics, p_value_populDiff = stats.ttest_ind( allPeaks[fam1], allPeaks[fam2],  equal_var=False )
                print(f"Welch's T-Test: {fam1} VS {fam2}: p_value = {p_value_populDiff}")

            else:
                statistics, p_value_populDiff = stats.mannwhitneyu( allPeaks[fam1], allPeaks[fam2] )
                print(f"Mann-Whitney_U: {fam1} VS {fam2}: p_value = {p_value_populDiff}")

#################################################################################################################################################################

    @staticmethod
    def boxplot_famABC_perCond( allResultsPSD : dict, index : int, participantNr : int ):

        allPeaks = Fam_VS_Fam.get_allPsdsABC_PerFam(allResultsPSD, index)

        data = {
            f"famA\n({BlockParams.FAM_A} Hz)"  : allPeaks["famA"],
            f"famB\n({BlockParams.FAM_B} Hz)"  : allPeaks["famB"],
            f"famC\n({BlockParams.FAM_C} Hz)"  : allPeaks["famC"],

        }
        Plots.boxplot( 
            data          = data, 
            title         = f"PSD per fam", # ignores whether fam has been target or not => all data included
            participantNr = participantNr, 
            ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
            xlabel        = f"", 
            axhline       = None
        )

#################################################################################################################################################################
  
