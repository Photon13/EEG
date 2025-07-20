from typing import List
import numpy as np

from RohBlock import RohBlock
from Berechnungen import Berechnungen


class Normierung:

    NORMIERUNGS_DIVIDENT_PARTICIANT_0 = None
    NORMIERUNGS_DIVIDENT_PARTICIANT_1 = None
    NORMIERUNGS_DIVIDENT_PARTICIANT_2 = None
    NORMIERUNGS_DIVIDENT_PARTICIANT_3 = None
    NORMIERUNGS_DIVIDENT_PARTICIANT_4 = None
    # WERDEN IN MAIN GENERIERT

    NormierungsDivident = [
        NORMIERUNGS_DIVIDENT_PARTICIANT_0, 
        NORMIERUNGS_DIVIDENT_PARTICIANT_1, 
        NORMIERUNGS_DIVIDENT_PARTICIANT_2, 
        NORMIERUNGS_DIVIDENT_PARTICIANT_3, 
        NORMIERUNGS_DIVIDENT_PARTICIANT_4
    ]


    @staticmethod
    def get_NormierungsDivident(rawFull, pathVMRK, n_blocks : int, blockLength : int):
        """ Output: Normierungsdivident (= mittlere PSD aller Blöcke [dB])"""
        list_means : List[float] = []

        for blockNr in range(n_blocks):  # berechne Durchschnitt für Block                                                            
            rawBlock = RohBlock.erzeuge_gecroppteRaw_fuerBlock(rawFull, pathVMRK, blockLength, blockNr )
            psds, psds_dB, freqs = Berechnungen.get_psds( rawBlock, blockLength )
            meanPSD = Normierung.berechneMean_Eintraege( psds_dB )
            list_means += meanPSD

        return Normierung.berechneMean_Eintraege( list_means )  #berechne Durchschnitt aller Blöcke


    @staticmethod
    def normiere_psds_dB( psds_dB : np.ndarray, normierungsDivident : float ) -> np.ndarray:
        psds_dB_normiert : List[float] = []
        for e in psds_dB:
            psds_normiert.append( e / normierungsDivident )  
        psds_normiert = np.array( psds_normiert )
        return psds_dB_normiert


    @staticmethod
    def berechneMean_Eintraege( arr : np.ndarray | List ):
        sum = 0.0
        for e in arr:
            sum += e
        mean = sum / float( len(arr) )
        return mean

