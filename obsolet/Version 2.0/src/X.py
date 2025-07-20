from typing import List
import numpy as np

class X: # keep!

    """
    famA = 33.0
    famB = 43.0
    famC = 53.0
    """

    @staticmethod
    def get_P_fLMR( freqComb : str, P_fABC : List[float] ):

        P_fA = P_fABC[0]
        P_fB = P_fABC[1]
        P_fC = P_fABC[2]

        famsLMR_per_freqCond : dict = {
            "ABC" : [ P_fA, P_fB, P_fC ],
            "ACB" : [ P_fA, P_fC, P_fB ],

            "BAC" : [ P_fB, P_fA, P_fC ],
            "BCA" : [ P_fB, P_fC, P_fA ],

            "CAB" : [ P_fC, P_fA, P_fB ],
            "CBA" : [ P_fC, P_fB, P_fA ] 
        }
        return famsLMR_per_freqCond[ freqComb ]
    

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

"""
############################################################################################# 

freqComb = "CBA"
target = "both"

P_fA = 2.0
P_fB = 4.0
P_fC = 6.0
P_fABC = np.array( [P_fA, P_fB, P_fC] )

############################################################################################# 

# CONVERT P_fABC TO Pf_fLMR:
P_fLMR = X.get_P_fLMR( freqComb, P_fABC )


#############################################################################################

# GET P_fTarget
arr = np.multiply(                      # set non-target streams to 0.0
    P_fLMR,                             # e.g. target="both"
    X.bool_targetPerCond[ target ]      # arr = [P_fL, 0.0, P_fR]
)

sum = np.sum( arr )                     # sum of power values for all target streams
n_values = np.count_nonzero( arr )      # number of target streams ( i.e. != 0.0 )
P_fTarget = sum / n_values              # mean power of target streams

#############################################################################################

#GET P_fNonTarget
arr = np.multiply(                      # set target streams to 0.0
    P_fLMR,                             # e.g. target="both"
    X.bool_nonTargetPerCond[ target ]   # arr = [0.0, P_fM, 0.0]
)

sum = np.sum( arr )                     # sum of power values for all non-target streams
n_values = np.count_nonzero( arr )      # number of non-target streams ( i.e. != 0.0 )
P_fTarget = sum / n_values              # mean power of non-target streams

#############################################################################################
"""