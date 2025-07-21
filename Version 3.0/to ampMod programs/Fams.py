from typing import List

class Fams:

    FAM_A = 35.9
    FAM_B = 39.7
    FAM_C = 43.1

    @staticmethod
    def get_fams_fromFreqComb( freqComb : str ) -> List[float]:
        famA = Fams.FAM_A
        famB = Fams.FAM_B
        famC = Fams.FAM_C
        
        famsLMR_per_freqCond : dict = {
            "ABC" : [ famA, famB, famC ],
            "ACB" : [ famA, famC, famB ],

            "BAC" : [ famB, famA, famC ],
            "BCA" : [ famB, famC, famA ],

            "CAB" : [ famC, famA, famB ],
            "CBA" : [ famC, famB, famA ] 
        }
        return famsLMR_per_freqCond[ freqComb ]