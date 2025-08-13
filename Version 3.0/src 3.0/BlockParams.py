from typing import List

class BlockParams:
    
    FAMS_ABC = { 
        "FAM_A" : 35.9, 
        "FAM_B" : 39.7, 
        "FAM_C" : 43.2
    }

    DEFAULT_N_BLOCKS = 3*4*6
    DEFAULT_BLOCK_LENGTH = 30 # [sec]

    ########################################################
    POSS_FREQ_COMBS : List[str] = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]

    POSS_TARGETS : List[str] = ["left", "middle", "right", "both"]

    POSS_TRIALS : List[int] = [1, 2, 3]

    def get_possFreqCombConds():
        poss_freqCombConds = []
        for fC in BlockParams.POSS_FREQ_COMBS:
            for target in BlockParams.POSS_TARGETS:
                poss_freqCombConds.append(f"{fC}_{target}")
        return poss_freqCombConds
    
print( len(BlockParams.get_possFreqCombConds()) )
print( BlockParams.get_possFreqCombConds() )