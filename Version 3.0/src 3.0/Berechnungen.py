import numpy as np
from typing import List

from Konvertierung import Konvertierung

class Berechnungen:

    def berechnePower_P_fABC( raw ):
        P_fA, P_fB, P_fC = berechnePower( raw) !
        P_fABC = np.array( [P_fA, P_fB, P_fC] )
        return P_fABC


    @staticmethod
    def bestimme_P_fTarget( P_fLMR : List[float], target : str ):
        """ Output: Mittlere Power für alle Target-Streams. """
        arr = np.multiply(                                  # set non-target streams to 0.0
            P_fLMR,                                         # e.g. target="both"
            Konvertierung.bool_targetPerCond[ target ]      # arr = [P_fL, 0.0, P_fR]
        )
        sum = np.sum( arr )                     # sum of power values for all target streams
        n_values = np.count_nonzero( arr )      # number of target streams ( i.e. != 0.0 )
        P_fTarget = sum / n_values              # mean power of target streams
        return P_fTarget


    @staticmethod
    def bestimme_P_fNonTarget( P_fLMR : List[float], target : str ):
        """ Output: Mittlere Power für alle Non-Target-Streams. """
        arr = np.multiply(                                  # set target streams to 0.0
            P_fLMR,                                         # e.g. target="both"
            Konvertierung.bool_nonTargetPerCond[ target ]   # arr = [0.0, P_fM, 0.0]
        )
        sum = np.sum( arr )                     # sum of power values for all non-target streams
        n_values = np.count_nonzero( arr )      # number of non-target streams ( i.e. != 0.0 )
        P_fNonTarget = sum / n_values              # mean power of non-target streams
        return P_fNonTarget