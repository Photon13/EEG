class BlockParams:
    
    #participant0:
    FAM_A = 33.0
    FAM_B = 43.0
    FAM_C = 53.0

    N_BLOCKS = 4*4
    BLOCK_LENGTH = 96 # [sec]

    #######################################################
    #participant 1-4:
    #FAM_A = 35.7
    #FAM_B = 40.1
    #FAM_C = 45.3

    #N_BLOCKS = 3*4*6
    #BLOCK_LENGTH = 30 # [sec]

    ########################################################
    freqCombs = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    freqComb : str

    conditions = ["left", "middle", "right", "both"]
    condition : int

    trials = [1, 2, 3]
    trial : int