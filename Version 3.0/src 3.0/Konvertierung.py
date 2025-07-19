import numpy as np
from typing import List

class Konvertierung:

    @staticmethod
    def get_P_fLMR( freqComb : str, P_fABC : List[float] ):

        P_fA = P_fABC[0]
        P_fB = P_fABC[1]
        P_fC = P_fABC[2]

        P_fLMR_per_freqCond : dict = {
            "ABC" : [ P_fA, P_fB, P_fC ],
            "ACB" : [ P_fA, P_fC, P_fB ],

            "BAC" : [ P_fB, P_fA, P_fC ],
            "BCA" : [ P_fB, P_fC, P_fA ],

            "CAB" : [ P_fC, P_fA, P_fB ],
            "CBA" : [ P_fC, P_fB, P_fA ] 
        }
        return P_fLMR_per_freqCond[ freqComb ]
    

    bool_targetPerCond : dict = {
        "left"   : np.array( [1, 0, 0] ),
        "middle" : np.array( [0, 1, 0] ),
        "right"  : np.array( [0, 0, 1] ),
        "both"   : np.array( [1, 0, 1] )
    }
    bool_nonTargetPerCond : dict = {
        "left"   : np.array( [0, 1, 1] ),
        "middle" : np.array( [1, 0, 1] ),
        "right"  : np.array( [1, 1, 0] ),
        "both"   : np.array( [0, 1, 0] )
    }