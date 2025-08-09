from F_Test import F_Test
from BlockParams import BlockParams

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

from itertools import combinations
from scipy import stats
from typing import List
import numpy as np
import re

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




class Fam_VS_Fam:

    @staticmethod
    def get_peakHight(allResultsPSD : List[dict], index : int, fam : int, freqCombCond : str, freqs : np.ndarray, psds : np.ndarray):
        return F_Test.get_peakHight(allResultsPSD, index, fam, freqCombCond, freqs, psds)
    


    @staticmethod
    def get_psdsABC_perFreqCombCond(allResultsPSD : List[dict], index : int ) -> dict:
        """ Output: {'ABC_left': [psd(famA), psd(famB), psd(famC)], 'ABC_middle': [psd(famA), psd(famB), psd(famC)] ... }"""
    
        psdsABC_perFreqCombCond = dict()
        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            psds  = allResultsPSD[index]["psdsDict"][freqCombCond]
            freqs = allResultsPSD[index]["freqsDict"][freqCombCond]

            psdsABC_perFreqCombCond[freqCombCond] = [0.0, 0.0, 0.0]
            for i in range( 3 ):
                psd_fam = Fam_VS_Fam.get_peakHight(allResultsPSD, index, BlockParams.FAMS_ABC[i], freqCombCond, freqs, psds)
                psdsABC_perFreqCombCond[freqCombCond][i] = psd_fam

        return psdsABC_perFreqCombCond



    @staticmethod
    def get_allPsdsPerFam( allResultsPSD : List[dict], index : int ) -> dict[List]:
        psdsABC_perFreqCombCond = Fam_VS_Fam.get_psdsABC_perFreqCombCond(allResultsPSD, index)

        allPeaks = {
            "famA" : [],
            "famB" : [],
            "famC" : []
        }
        for freqCombCond in psdsABC_perFreqCombCond:
            allPeaks["famA"].append( psdsABC_perFreqCombCond[freqCombCond][0] )
            allPeaks["famB"].append( psdsABC_perFreqCombCond[freqCombCond][1] )
            allPeaks["famC"].append( psdsABC_perFreqCombCond[freqCombCond][2] )

        return allPeaks



    @staticmethod
    def test_whetherPeaksFamABC_sigDifferent(allResultsPSD : List[dict], index : int):

        allPeaks = Fam_VS_Fam.get_allPsdsPerFam(allResultsPSD, index)

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



    @staticmethod
    def plot_peaks_famABC(allResultsPSD : List[dict], index : int):
        allPeaks = Fam_VS_Fam.get_allPsdsPerFam(allResultsPSD, index)
        peaks_famABC = [allPeaks["famA"], allPeaks["famB"], allPeaks["famC"]]
        participantNr = str(re.findall( r"\d+", allResultsPSD[index]["file_id"] )[0])
        plt.boxplot(peaks_famABC)
        plt.xticks([1, 2, 3], ["famA", "famB", "famC"])
        plt.title(f"PSD per fam, participant{participantNr}", fontsize=14, fontweight='bold', pad=20 )
        plt.ylabel(r"$PSD$ [$\frac{V^{2}}{Hz}$]", fontsize=12)
        plt.show()
        inp = input("any ")


  
