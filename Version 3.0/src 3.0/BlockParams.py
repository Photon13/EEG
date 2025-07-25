class BlockParams:
    
    FAM_A = 35.9
    FAM_B = 39.7
    FAM_C = 43.2

    N_BLOCKS = 3*4*6
    BLOCK_LENGTH = 30 # [sec]

    ########################################################
    freqCombs = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    freqComb : str

    conditions = ["left", "middle", "right", "both"]
    condition : int

    trials = [1, 2, 3]
    trial : int