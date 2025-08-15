from typing import List

class BlockParams:
    
    FAMS_ABC = { 
        "FAM_A" : 35.9, 
        "FAM_B" : 39.7, 
        "FAM_C" : 43.2
    }
    FAMS_ABC_LIST = [ FAMS_ABC["FAM_A"], FAMS_ABC["FAM_B"], FAMS_ABC["FAM_C"] ]

    DEFAULT_N_BLOCKS     : int = 3*4*6
    DEFAULT_BLOCK_LENGTH : int = 30 # [sec]
    DEFAULT_SFREQ   : float = 500.0

    ########################################################
    POSS_FREQ_COMBS : List[str] = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    POSS_TARGETS    : List[str] = ["left", "middle", "right", "both"]
    POSS_TRIALS     : List[int] = [1, 2, 3]

    @staticmethod #korrekt
    def get_possFreqCombConds():
        poss_freqCombConds = []
        for fC in BlockParams.POSS_FREQ_COMBS:
            for target in BlockParams.POSS_TARGETS:
                poss_freqCombConds.append(f"{fC}_{target}")
        return poss_freqCombConds
    
    @staticmethod #korrekt
    def get_musterDict():
        musterDict = {}
        for freqCombCond in BlockParams.get_possFreqCombConds():
            musterDict[freqCombCond] = {
                "trial0" : None, # for concatenated Version
                "trial1" : None,
                "trial2" : None,
                "trial3" : None
            }
        return musterDict
