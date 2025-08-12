from typing import List
import numpy as np
import scipy
from scipy import stats


COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



class F_Test:

    MAX_DIST_FROM_FAM = 2
    N_INCLUDE_PER_SIDE = 60   # ca 0.25 Hz
    N_IGNORE = 2

    @staticmethod
    def inspect_rangeAroundFam( whichToPrint : str, fam : float, freqs : np.ndarray, psds : np.ndarray ):
        """ whichToPrint = \"freqs\" | \"psds\" """

        # find index of frequency bin closest to stimulation frequency
        i_bin_fam = np.argmin( abs(freqs - fam) )
        #print(COLORPURPLE + f"{i_bin_fam}" + COLOREND)

        freqs_inRange     = list()
        psds_inRange      = list()

        n_neighbours_perSide = 60


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



    @staticmethod
    def get_indexLargestValue_nextFam(fam : int, maxDistFromFam : int, freqs : np.ndarray, psds : np.ndarray):
        # find index of frequency bin closest to stimulation frequency
        i_bin_fam = np.argmin( abs(freqs - fam) )

        n_neighbours_perSide = maxDistFromFam # max. erlaubter Abstand von Fam in Abtastunkten
        # Bsp. maxDistFromFam = 2:
        # Erste und zweite freq links & rechts von fam werden auch berücksichtigt
        # Falls die psd einer dieser freqs größer ist als psd(fam), dann wird diese freq stattdessen genutzt
        # Kompensation für leichte Bew. (Doppler-Effekt), sowie Spannungs-Abweichungen im Lautsprecher oder Prozessor-Output
        # Abstand von 1 Bin entspricht ca. 0.0038 Hz (d.h. f_n - f_n-1 bzw. f_n - f_n+1), 
        # d.h. bei 2 Nachbarn wird Abweichung von ca. 0.0074 Hz von fam pro Seite toleriert

        helpList = list( range( (-n_neighbours_perSide), (+n_neighbours_perSide)+1 ) ) #-2 bis +2

        psds_cropped = list()
        for i in helpList:
            psds_cropped.append(psds[i_bin_fam + i])
        #print(psds_cropped)

        np.argmax(psds_cropped)  #zw 0 und 4
        delta = np.argmax(psds_cropped) - 2 #zw. -2 und 2
        i_largestVal = i_bin_fam + delta

        return i_largestVal


    @staticmethod
    def get_PSDneighbours(i_largestVal : int, n_ignore :int, n_includePerSide : int, psds : np.ndarray):

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
    


    @staticmethod
    def get_peakHight( psds : np.ndarray, freqs : np.ndarray, fam : float ) -> float:
        i_largestVal    = F_Test.get_indexLargestValue_nextFam(fam, F_Test.MAX_DIST_FROM_FAM, freqs, psds)
        return float(psds[i_largestVal])
    



    @staticmethod
    def one_sidedANOVA(allResultsPSD : List[dict], index : int, freqCombConds : List[str], fams_ABC : List[float]) -> dict:

        maxDistFromFam    = F_Test.MAX_DIST_FROM_FAM
        n_includePerSide  = F_Test.N_INCLUDE_PER_SIDE
        n_ignore          = F_Test.N_IGNORE

        count_sig = 0
        count_nonSig = 0
        count_invalid = 0

        sig_pValsDict     = dict()
        nonSig_pValsDict  = dict()
        invalid_pValsDict = dict()


        for freqCombCond in freqCombConds:
            for fam in fams_ABC:

                psds  = allResultsPSD[index]["psdsDict"][freqCombCond]
                freqs = allResultsPSD[index]["freqsDict"][freqCombCond]

                i_largestVal       = F_Test.get_indexLargestValue_nextFam( fam, maxDistFromFam, freqs, psds )
                psds_neighbours    = F_Test.get_PSDneighbours( i_largestVal, n_ignore, n_includePerSide, psds )
                psd_peak           = F_Test.get_peakHight( allResultsPSD, index, fam, freqCombCond, freqs, psds )
                statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                if( type(p_value) != np.float64 ):
                    count_invalid += 1
                    if( invalid_pValsDict.get(freqCombCond) == None ):
                        invalid_pValsDict[freqCombCond] = dict()
                    invalid_pValsDict[freqCombCond][fam] = p_value

                elif( 0.05 > round(p_value, 1) ):
                    count_sig += 1
                    if( sig_pValsDict.get(freqCombCond) == None ):
                        sig_pValsDict[freqCombCond] = dict()
                    sig_pValsDict[freqCombCond][fam] = p_value

                else:
                    count_nonSig += 1
                    if( nonSig_pValsDict.get(freqCombCond) == None ):
                        nonSig_pValsDict[freqCombCond] = dict()
                    nonSig_pValsDict[freqCombCond][fam] = p_value

        
        anovaDict = {
            "file_id"              : allResultsPSD[index]["file_id"],
            "index allResultsDict" : index,
            "maxDistFromFam"       : maxDistFromFam,
            "n_includePerSide"     : n_includePerSide,
            "n_ignore"             : n_ignore,
            "count_sig"            : count_sig,
            "count_nonSig"         : count_nonSig,
            "count_invalid"        : count_invalid,
            "sig_pValsDict"        : sig_pValsDict,
            "nonSig_pValsDict"     : nonSig_pValsDict,
            "invalid_pValsDict"    : invalid_pValsDict
        }
        return anovaDict
    



