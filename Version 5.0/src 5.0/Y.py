from Statistics import Statistics

from typing import List
import numpy as np
import copy
import re

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



class Y:

    @staticmethod
    def convert_perFreqCombCond_to_perCond( dictPerFreqCombCond ):

        subKeys = []
        for freqCombCond in dictPerFreqCombCond:
            for subKey in dictPerFreqCombCond[freqCombCond]:
                if( subKey not in subKeys ):
                    subKeys.append(subKey)

        subDict = {}
        for subKey in subKeys:
            subDict[subKey] = []

        dictPerCond = {
            "left" : copy.deepcopy(subDict),
            "middle" : copy.deepcopy(subDict),
            "right" : copy.deepcopy(subDict),
            "both" : copy.deepcopy(subDict)
        }
        for freqCombCond in dictPerFreqCombCond:
            cond = str( re.findall( r"(left|middle|right|both)", freqCombCond )[0] ) 

            for subKey in subKeys:
                newEntry = dictPerFreqCombCond[freqCombCond][subKey] 

                if( type(newEntry) == float or type(newEntry) == np.float64 ):
                    dictPerCond[cond][subKey].append( newEntry )

                elif( type(newEntry) == List or type(newEntry) == list ):
                    dictPerCond[cond][subKey].extend( newEntry )
                else:
                    print(COLORRED + f"Invalid data type {type(newEntry)} for appendage. " + COLOREND + "Message from convert_perFreqCombCond_to_perCond." )

        return dictPerCond


    @staticmethod
    def get_allPeaks ( dictPerFreqCombCond ):
        allPeaks = {}

        subKeys = []
        for freqCombCond in dictPerFreqCombCond:
            for subKey in dictPerFreqCombCond[freqCombCond]:
                if( subKey not in subKeys ):
                    subKeys.append( subKey )


        for subKey in subKeys:
            allPeaks[subKey] = []

        for freqCombCond in dictPerFreqCombCond:
            for subKey in subKeys:
                newEntry = dictPerFreqCombCond[freqCombCond][subKey]
                
                if( type(newEntry) == float or type(newEntry) == np.float64 ):
                    allPeaks[subKey].append( newEntry )

                elif( type(newEntry) == List or type(newEntry) == list ):
                    allPeaks[subKey].extend( newEntry )
                else:
                    print(COLORRED + f"Invalid data type {type(newEntry)} for appendage. " + COLOREND + "Message from get_allPeaks." )

        return allPeaks
    

    @staticmethod
    def test_sigDiff_betweenConds_perFam( dictFamsPerCond ):

        famNames = []
        for cond in dictFamsPerCond:
            for famName in dictFamsPerCond[cond]:
                if( famName not in famNames ):
                    famNames.append(famName)

        for famName in famNames:
            print(COLORCYAN + f"\nTest sigDiff {famName} between conditions:" + COLOREND)

            p_values_shapiro = []
            for cond in ["left", "middle", "right", "both"]:
                p_values_shapiro.append( Statistics.shapiroWilk( dictFamsPerCond[cond][famName], f"{famName}" ) )

                
            if all( p_value > 0.05 for p_value in p_values_shapiro ):
                method = "t-test"
            else:
                method = "mann-whitney-u"
            
            data = {
                "condition : \'target = left\'"   : dictFamsPerCond["left"][famName], 
                "condition : \'target = middle\'" : dictFamsPerCond["middle"][famName],
                "condition : \'target = right\'"  : dictFamsPerCond["right"][famName],
                "condition : \'target = both\'"   : dictFamsPerCond["both"][famName]
            }
            Statistics.test_sigDifference( data, method )


    def test_sigDiff_betweenFams( allPeaks ):

        famNames = []
        for famName in allPeaks:
            if( famName not in famNames ):
                famNames.append(famName)

        for famName in famNames:
            print(COLORCYAN + f"\nTest sigDiff between fams:" + COLOREND)

            p_values_shapiro = []
            for cond in ["left", "middle", "right", "both"]:
                p_values_shapiro.append( Statistics.shapiroWilk( allPeaks[famName], f"{famName}" ) )

                
            if all( p_value > 0.05 for p_value in p_values_shapiro ):
                method = "t-test"
            else:
                method = "mann-whitney-u"
            
        data = {}
        for famName in famNames:
                data[famName] = allPeaks[famName]

        Statistics.test_sigDifference( data, method )
                