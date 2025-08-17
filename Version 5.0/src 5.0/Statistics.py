from scipy import stats
import numpy as np
from typing import List
from itertools import combinations

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'

class Statistics:

    def shapiroWilk( data, label : str ):
        statistics, p_value = stats.shapiro( data )
        #print(f"Shapiro-Wilk: p_value {label} = {p_value}")
        return p_value


    def test_sigDifference( data : dict, method: str ):
        """ Method: \"t-test\" | \"mann-whitney-u\" """
        labels = list(data.keys())
        combos = list( combinations( labels, 2) )
        for combo in combos:
            label1, label2 = combo[0], combo[1]

            if( method == "t-test"):
                statistics, p_value = stats.ttest_ind( data[label1], data[label2],  equal_var=False )
                print(f"\nWelch's T-Test: {label1} VS {label2}: p_value = {p_value}")
            else:
                statistics, p_value = stats.ttest_ind( data[label1], data[label2],  equal_var=False )
                print(f"\nMann-Whitney_U: {label1} VS {label2}: p_value = {p_value}")

            mean1, mean2 = np.mean(data[label1]), np.mean(data[label2])
            sign = "=" #default
            if( p_value <= 0.05 ):
                if( mean1 > mean2 ):
                    sign = ">"
                elif( mean1 < mean2):
                    sign = "<"
                print(COLORPURPLE, end="")    
            print(f"    {mean1} {sign} {mean2}"   + COLOREND)


