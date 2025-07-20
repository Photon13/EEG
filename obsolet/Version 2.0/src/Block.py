from typing import List
import mne
import numpy as np

from Matrices import Matrices

class Block:

    freqComb  : List[str]
    condition : str

    raw : mne.io.Raw

    startSample : int   # bezogen auf original rawFull
    endSample   : int   # 

    startTime : float   # bezogen auf original rawFull
    endTime   : float   #

    power_fABC : List[float]    # bzw. PSD oder andere Größe
    power_fLMR : List[float]    # CAVE: Normierung !

    power_fTarget     : List[float]
    power_fNon_Target : List[float]

    def __init__(self):
        self.freqComb  = None
        self.condition = None

        self.matrix_pos_fx = None
        #

        self.raw = None

        self.startSample = None
        self.endSample   = None

        self.startTime = None
        self.endTime   = None

        self.power_fABC = None
        self.power_fLMR = None

        self.power_fTarget     = None
        self.power_fNon_Target = None


    def set_freqComb (self, freqComb : List[str] ):
        """ freqComb E { ["ABC"], ["ACB"], ... ["CBA"] } """
        self.freqComb = freqComb
    
    def set_matrix_pos_fx( self ):
        if( self.freqComb == "ABC" ):
            self.matrix_pos_fx = Matrices.MatrixABC.pos_fx



    def set_condition( self, condition : str ):

    #def set_power_fABC():

    #def gen_power_fLMR(self):
        return np.array(self.power_fABC) * self.matrix_pos_fx # Multiplikation korrekt? CAVE: Liste * Matrix




class Blocks:

    N_TRIALS = 3
    N_CONDITIONS = 4
    N_FREQ_COMBS = 6

    N_BLOCKS : int = N_TRIALS * N_CONDITIONS * N_FREQ_COMBS

    blocks : dict[Block]

    def __init__(self):
        self.blocks = Blocks.gen_blocks()

    @staticmethod
    def gen_blocks():
        blocks : dict[Block] = {}
        for b in range( Blocks.N_BLOCKS ):
            blocks[f"block{b}"] = Block()
        return blocks





#blocksParticipant0 : Blocks = Blocks()
#print( blocksParticipant0.blocks["block0"].freqComb )

#blocksParticipant0.blocks["block0"].set_freqComb(["A","B","C"])
#print( blocksParticipant0.blocks["block0"].freqComb )