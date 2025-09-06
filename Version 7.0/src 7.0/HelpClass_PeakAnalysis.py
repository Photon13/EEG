import numpy as np
from typing import List

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



class HelpClass_PeakAnalysis:

    @staticmethod
    def get_peakAnalysisParams( ):
        """ trialType = "trial0" | "trial123" """

        toleratedPeakDeviation = 1
        n_includePerSide = 30 # 3 Hz
        n_ignore = 1

        return toleratedPeakDeviation, n_includePerSide, n_ignore


    @staticmethod
    def inspect_rangeAroundFam( whichToPrint : str, n_neighbours_perSide : int, fam : float, freqs : np.ndarray, psds : np.ndarray ):
        """ whichToPrint = \"freqs\" | \"psds\" """

        i_bin_fam = np.argmin( abs(freqs - fam) ) # find index of frequency bin closest to stimulation frequency

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
        
        i_bin_fam = np.argmin( abs(freqs - fam) ) # find index of frequency bin closest to stimulation frequency

        toleratedPeakDeviation, n_includePerSide, n_ignore = HelpClass_PeakAnalysis.get_peakAnalysisParams( )
        tolDev = toleratedPeakDeviation # max. erlaubter Abstand von Fam in Abtastunkten

        i_largestVal = i_bin_fam
        for i in range( (i_bin_fam - tolDev), (i_bin_fam + tolDev)+1):
            if( psds[i] > i_largestVal ):
                i_largestVal = psds[i]

        return i_largestVal
    


    @staticmethod
    def get_PSDneighbours( fam : int, psds : np.ndarray, freqs : np.ndarray ):

        i_largestVal = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
        toleratedPeakDeviation, n_includePerSide, n_ignore = HelpClass_PeakAnalysis.get_peakAnalysisParams()
        

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