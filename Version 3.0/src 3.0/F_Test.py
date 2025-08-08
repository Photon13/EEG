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
    def get_indexLargestValue_nextFam(fam : int, freqs : np.ndarray, psds : np.ndarray):
        # find index of frequency bin closest to stimulation frequency
        i_bin_fam = np.argmin( abs(freqs - fam) )

        n_neighbours_perSide = 2 # max. erlaubter Abstand von Fam in Abtastunkten
        # Erste und zweite freq links & rechts von fam werden auch berücksichtigt
        # Falls die psd einer dieser freqs größer ist als psd(fam), dann wird diese freq stattdessen genutzt
        # Kompensation für leichte Bew. (Doppler-Effekt), sowie Spannungs-Abweichungen im Lautsprecher oder Prozessor-Output
        # Abstand von 2 Bins entspricht ca. 0.0038 Hz, d.h. bei 2 Nachbarn wird Abweichung von ca. 0.0074 Hz von fam pro Seite toleriert

        helpList = list( range( (-n_neighbours_perSide), (+n_neighbours_perSide)+1 ) ) #-2 bis +2

        psds_cropped = list()
        for i in helpList:
            psds_cropped.append(psds[i_bin_fam + i])
        print(psds_cropped)

        np.argmax(psds_cropped)  #zw 0 und 4
        delta = np.argmax(psds_cropped) - 2 #zw. -2 und 2
        i_largestVal = i_bin_fam + delta

        return i_largestVal


    def get_PSDneighbours(i_largestVal : int, n_ignore :int, n_includePerSide : int, freqs : np.ndarray, psds : np.ndarray):

        i_incl_u2 = i_largestVal + n_ignore + n_includePerSide   #  erste includierte upperRange
        i_incl_u1 = i_largestVal + n_ignore + 1                  # letzte includierte upperRande
        
        i_incl_l2 = i_largestVal - n_ignore - n_includePerSide   #  erste includierte lowerRange
        i_incl_l1 = i_largestVal - n_ignore - 1                  # letzte includierte lowerRange

        i_upperRange = list( range( (i_incl_u1), (i_incl_u2)+1 ) ) 
        i_lowerRange = list( range( (i_incl_l2), (i_incl_l1)+1 ) )

        #print(len(i_lowerRange))
        #print(len(i_upperRange))
        #print(i_lowerRange)
        #print(i_upperRange) #stimmt

        psds_neighbours = list()
        for i in i_upperRange:
            psds_neighbours.append(psds[i])
        for i in i_lowerRange:
            psds_neighbours.append(psds[i])
        return np.array(psds_neighbours)

