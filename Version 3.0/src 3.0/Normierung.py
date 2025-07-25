from typing import List
import numpy as np

from RohBlock import RohBlock
from Berechnungen import Berechnungen
from HelpMethods import HelpMethods


class Normierung:

    NormierungsDivident = {
        "participant0" : 12.829149943758924,
        "participant1" : None,
        "participant2" : None,
        "participant3" : None,
        "participant4" : None,
        "participant13" : -12.678245635897781
    }
    # WERDEN IN MAIN GENERIERT


    @staticmethod
    def get_NormierungsDivident(rawFull, pathVMRK, n_blocks : int, blockLength : int):
        """ Output: Normierungsdivident (= mittlere PSD aller Blöcke [dB])"""
        list_means : List[float] = []

        for blockNr in range(n_blocks):  # berechne Durchschnitt für Block                                                            
            rawBlock = RohBlock.erzeuge_gecroppteRaw_fuerBlock(rawFull, pathVMRK, blockLength, blockNr )
            psds, psds_dB, freqs = Berechnungen.get_psds( rawBlock, blockLength )
            meanPSD = HelpMethods.berechneMean_Eintraege( psds_dB )
            list_means.append(meanPSD)
            
            print(f"blockNr = {blockNr}")
            print(f"list_means = {list_means}")
            
        return HelpMethods.berechneMean_Eintraege( list_means )  #berechne Durchschnitt aller Blöcke


    @staticmethod
    def normiere_psds_dB( psds_dB : np.ndarray, normierungsDivident : float ) -> np.ndarray:
        psds_dB_normiert : List[float] = []
        for e in psds_dB:
            psds_dB_normiert.append( e / normierungsDivident )  
        psds_dB_normiert = np.array( psds_dB_normiert )
        return psds_dB_normiert



