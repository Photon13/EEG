from Statistics import Statistics
from BlockParams import BlockParams
from X import HelpClass_PeakAnalysis
from Plots import Plots

from scipy import stats
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


    @staticmethod
    def test_sigDiff_betweenFams( allPeaks ):

        famNames = []
        for famName in allPeaks:
            if( famName not in famNames ):
                famNames.append(famName)

        print(COLORCYAN + f"\nTest sigDiff between fams:" + COLOREND)
        for famName in famNames:
            
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


    @staticmethod
    def boxplot_fam_perCond( dictPerCond : dict[List], participantNr : int ) -> None:
        
        fams = []
        for freqCombCond in dictPerCond:
            for fam in dictPerCond[freqCombCond]:
                if( fam not in fams ):
                    fams.append(fam)

        
        for fam in fams:
            data = {
                "left"   : dictPerCond["left"][fam],
                "middle" : dictPerCond["middle"][fam],
                "right"  : dictPerCond["right"][fam],
                "both"   : dictPerCond["both"][fam]
            }
            Plots.boxplot( 
                data          = data, 
                title         = f"PSD({fam}) per condition", # ignores whether fam has been target or not => all data included
                participantNr = participantNr, 
                ylabel        = r"$PSD$ [$\frac{V^{2}}{Hz}$]", 
                xlabel        = f"Condition", 
                axhline       = None
            )
                

    @staticmethod
    def test_sigHigherThanNoise( allResultsPSD : List[dict], index : int ) -> None:

        print(COLORGREEN  + "\n\nTest whether PSD of famA, famB or famC sig. higher than noise" + COLOREND)

        #################################################################
        print(COLORYELLOW  + "\nallGoodBlocksConcat: " + COLOREND)
        count_sig    = 0
        count_nonSig = 0
  
        psds  = allResultsPSD[index]["psds_concatAllGoodBlocks"]
        freqs = allResultsPSD[index]["freqs_concatAllGoodBlocks"]

        for fam in BlockParams.FAMS_ABC_LIST:
            count_sig, count_nonSig = Y.increase_properCount( psds, freqs, fam, count_sig, count_nonSig )

        print(COLORCYAN   + f"count_sig = {count_sig}"       + COLOREND)
        print(COLORCYAN   + f"count_nonSig = {count_nonSig}\n" + COLOREND)


        #################################################################
        print(COLORYELLOW  + "\ntrialsConcat: " + COLOREND)
        count_sig    = 0
        count_nonSig = 0

        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            for trial in allResultsPSD[index]["psdsDict"][freqCombCond]:
                if( trial == "trial0" ):

                    psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
                    freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]

                    for fam in BlockParams.FAMS_ABC_LIST:
                        count_sig, count_nonSig = Y.increase_properCount( psds, freqs, fam, count_sig, count_nonSig )

        print(COLORCYAN   + f"count_sig = {count_sig}"       + COLOREND)
        print(COLORCYAN   + f"count_nonSig = {count_nonSig}\n" + COLOREND)


        #################################################################
        print(COLORYELLOW  + "\ntrials separately: " + COLOREND)
        count_sig    = 0
        count_nonSig = 0

        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            for trial in allResultsPSD[index]["psdsDict"][freqCombCond]:
                if( trial == "trial1" or trial == "trial2" or trial == "trial3" ):

                    psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
                    freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]

                    for fam in BlockParams.FAMS_ABC_LIST:
                        count_sig, count_nonSig = Y.increase_properCount( psds, freqs, fam, count_sig, count_nonSig )

        print(COLORCYAN   + f"count_sig = {count_sig}"       + COLOREND)
        print(COLORCYAN   + f"count_nonSig = {count_nonSig}\n" + COLOREND)



    @staticmethod
    def increase_properCount( psds, freqs, fam, count_sig, count_nonSig ): 
        """ Help fct for test_sigHigherThanNoise() """
        i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
        psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
        psd_peak           = psds[i_largestVal]

        statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

        if( 0.05 < round(p_value, 1) ):
            count_sig += 1
        else:
            count_nonSig += 1
            
        return count_sig, count_nonSig