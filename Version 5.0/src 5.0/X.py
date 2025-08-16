from typing import List
import numpy as np
import copy
import re
import scipy
from scipy import stats

from BlockParams import BlockParams
from Statistics import Statistics
from Plots import Plots


COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


class HelpClass_PeakAnalysis:

    TOLERATED_PEAK_DEVIATION = 1
    N_INCLUDE_PER_SIDE = 60 #1.33333 Hz
    N_IGNORE = 2
    # two bins are ca. 0.0111 Hz apart

    #for trials123 : 1, 20, 1 

    @staticmethod
    def inspect_rangeAroundFam( whichToPrint : str, n_neighbours_perSide : int, fam : float, freqs : np.ndarray, psds : np.ndarray ):
        """ whichToPrint = \"freqs\" | \"psds\" """

        # find index of frequency bin closest to stimulation frequency
        i_bin_fam = np.argmin( abs(freqs - fam) )
        #print(COLORPURPLE + f"{i_bin_fam}" + COLOREND)

        freqs_inRange     = list()
        psds_inRange      = list()

        for i in range(i_bin_fam - n_neighbours_perSide, i_bin_fam + n_neighbours_perSide+1):
            freqs_inRange.append( freqs[i] )
            psds_inRange.append(  psds[i] )

        if( whichToPrint == "freqs" ):
            printList      = freqs_inRange
            i_largestValue = np.argmax(psds_inRange) #sic

        if( whichToPrint == "psds" ):
            printList      = psds_inRange
            i_largestValue = np.argmax(psds_inRange)

        for j in range( 0, len(printList) ):
            if( j == n_neighbours_perSide ):
                print(COLORPURPLE, end = " ")
            elif( j == i_largestValue ):
                print(COLORRED, end = " ")
            else:
                print(COLORCYAN, end = " ")
            print( printList[j], end = " " )
            print(COLOREND)



    @staticmethod
    def get_indexLargestValue_nextFam( fam : int, psds : np.ndarray, freqs : np.ndarray ):
        # find index of frequency bin closest to stimulation frequency
        i_bin_fam = np.argmin( abs(freqs - fam) )

        tolDev = HelpClass_PeakAnalysis.TOLERATED_PEAK_DEVIATION # max. erlaubter Abstand von Fam in Abtastunkten
        # Bsp. maxDistFromFam = 2:
        # Erste und zweite freq links & rechts von fam werden auch berücksichtigt
        # Falls die psd einer dieser freqs größer ist als psd(fam), dann wird diese freq stattdessen genutzt
        # Kompensation für leichte Bew. (Doppler-Effekt), sowie Spannungs-Abweichungen im Lautsprecher oder Prozessor-Output
        # Abstand von 1 Bin entspricht ca. 0.0038 Hz (d.h. f_n - f_n-1 bzw. f_n - f_n+1), 
        # d.h. bei 2 Nachbarn wird Abweichung von ca. 0.0074 Hz von fam pro Seite toleriert

        i_largestVal = i_bin_fam
        for i in range( (i_bin_fam - tolDev), (i_bin_fam + tolDev)+1):
            if( psds[i] > i_largestVal ):
                i_largestVal = psds[i]

        return i_largestVal
    


    @staticmethod
    def get_PSDneighbours( fam : int, psds : np.ndarray, freqs : np.ndarray ):

        i_largestVal = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
        n_includePerSide = HelpClass_PeakAnalysis.N_INCLUDE_PER_SIDE
        n_ignore = HelpClass_PeakAnalysis.N_IGNORE
        

        i_incl_u2 = i_largestVal + n_ignore + n_includePerSide   #  erste includierte upperRange
        i_incl_u1 = i_largestVal + n_ignore + 1                  # letzte includierte upperRande
        
        i_incl_l2 = i_largestVal - n_ignore - n_includePerSide   #  erste includierte lowerRange
        i_incl_l1 = i_largestVal - n_ignore - 1                  # letzte includierte lowerRange

        i_upperRange = list( range( (i_incl_u1), (i_incl_u2)+1 ) ) 
        i_lowerRange = list( range( (i_incl_l2), (i_incl_l1)+1 ) )


        psds_neighbours = list()
        for i in i_upperRange:
            psds_neighbours.append(psds[i])
        for i in i_lowerRange:
            psds_neighbours.append(psds[i])
        return np.array(psds_neighbours)
    

    @staticmethod #works
    def covert_psdsABC_to_psds_LMR( freqCombCond : str, psdsABC : dict ) -> List[float]:

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


#############################################################################################################################    
#############################################################################################################################
#############################################################################################################################


class PeaksABC:

    @staticmethod
    def get_psdsABC_perFreqCombCond( allResultsPSD : List[dict], index : int, trials : List[str] ) -> dict[dict]:
        """ Output: {'ABC_left': {'famA': [...], 'famB' : [...], 'famC' : [...]}, 'ABC_middle': {...} ... }"""
    
        psdsABC_perFreqCombCond = dict()

        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            psdsABC_perFreqCombCond[freqCombCond] = {
                "famA" : [],
                "famB" : [],
                "famC" : []
            }

        for freqCombCond in allResultsPSD[index]["psdsDict"]:
            for trial in trials:

                psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
                freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]

                famNames = ["famA", "famB", "famC"]
                for i in range( 3 ):
                    fam = BlockParams.FAMS_ABC_LIST[i]

                    i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                    psdsABC_perFreqCombCond[freqCombCond][famNames[i]].append( psds[i_largestVal] )
                    
        return psdsABC_perFreqCombCond
    

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


class PeaksLMR:

    @staticmethod
    def get_psdsLMR_perFreqCombCond( psdsABC_perFreqCombCond : dict[dict] ) -> dict[dict]:

        psdsLMR_perFreqCombCond = dict()
        for freqCombCond in psdsABC_perFreqCombCond:
            psdsABC = psdsABC_perFreqCombCond[freqCombCond]

            psdsLMR : dict = HelpClass_PeakAnalysis.covert_psdsABC_to_psds_LMR(freqCombCond, psdsABC)
            psdsLMR_perFreqCombCond[freqCombCond] = psdsLMR

        return psdsLMR_perFreqCombCond


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


class PeaksTnT:

    @staticmethod
    def get_psdsTnT_perFreqCombCond( psdsLMR_perFreqCombCond : dict[dict] ) -> dict[dict]:

        psdsTnT_perFreqCombCond = dict()
        for freqCombCond in psdsLMR_perFreqCombCond:
            psds_LMR : dict = psdsLMR_perFreqCombCond[freqCombCond]

            psdsTnT_perFreqCombCond[freqCombCond] = HelpClass_PeakAnalysis.calc_psdTarget_nonTarget(freqCombCond, psds_LMR)
        return psdsTnT_perFreqCombCond
    

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


class StatisticsPeaks:

    @staticmethod # F-TEST
    def test_famABC_sigHigher_thanNoise( allResultsPSD : List[dict], index : int, trials : List[str] | None ) -> None:

        count_sig    = 0
        count_nonSig = 0

        list_sig     = []
        list_nonSig  = []


        if( trials == None ):
            psds  = allResultsPSD[index]["psds_concatAllGoodBlocks"]
            freqs = allResultsPSD[index]["freqs_concatAllGoodBlocks"]

            for fam in BlockParams.FAMS_ABC_LIST:

                i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                psd_peak           = psds[i_largestVal]

                statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                if( 0.05 < round(p_value, 1) ):
                    count_sig += 1
                    list_sig.append(f"fam {fam}")
                else:
                    count_nonSig += 1
                    list_nonSig.append(f"fam {fam}")


        else:
            for freqCombCond in allResultsPSD[index]["psdsDict"]:
                for trial in trials:

                    psds  = allResultsPSD[index]["psdsDict"][freqCombCond][trial]
                    freqs = allResultsPSD[index]["freqsDict"][freqCombCond][trial]

                    for fam in BlockParams.FAMS_ABC_LIST:

                        i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                        psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                        psd_peak           = psds[i_largestVal]

                        statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                        if( 0.05 < round(p_value, 1) ):
                            count_sig += 1
                            list_sig.append(f"{freqCombCond}_{trial}_{fam}")
                        else:
                            count_nonSig += 1
                            list_nonSig.append(f"{freqCombCond}_{trial}_{fam}")


        print(COLORGREEN  + "Test whether PSD of famA, famB or famC sig. higher than noise" + COLOREND)
        print(COLORCYAN   + f"count_sig = {count_sig}"       + COLOREND)
        print(COLORCYAN   + f"count_nonSig = {count_nonSig}" + COLOREND)
        print("\n")
        print(COLORYELLOW + f"list_sig = {list_sig}"         + COLOREND)
        print("\n")
        print(COLORYELLOW + f"list_nonSig = {list_nonSig}"   + COLOREND)







    #test sig difference famA VS famB VS famC
    #test sig difference famLeft VS famMiddle VS famRight







    @staticmethod
    def testSigDifferent_target_VS_nonTarget( psdsTnT_perCond : dict[dict] ) -> None:
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
    def testSigDifferent_quotient_VS_quotient( psdsTnT_perCond : dict[dict] ) -> None:
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



