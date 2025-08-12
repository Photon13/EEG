from BlockParams import BlockParams
from Ereignisse import Ereignisse

from typing import List
import mne
import copy

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'

class RohBlock:

    @staticmethod
    def getBlockStartAndEnd( blockNr, samplerate, blockLength, pathVMRK ):
        zBusses = Ereignisse.get_zBusse( pathVMRK )
        start = float( zBusses[ blockNr ] ) / float( samplerate )
        end = start + blockLength
        return start, end
    
    @staticmethod
    def erzeuge_gecroppteRaw_fuerBlock(rawFull, pathVMRK, blockLength, blockNr ):
        start, end = RohBlock.getBlockStartAndEnd(blockNr, rawFull.info["sfreq"], blockLength, pathVMRK)
        rawBlock = rawFull.copy().crop(tmin = start, tmax = end)
        return rawBlock
    


    @staticmethod #korrekt
    def get_rawsPerFreqCombCond( rawFull : mne.io.Raw, pathVMRK : str , blockDict : dict, blockLength : int ):
        raws_perFreqCombCond = list()
        freqCombCond_list    = list()
        trial_list           = list()

        for blockNr in range(72):
            freqComb  = blockDict[f"block{blockNr}"]["freqComb"]
            condition = blockDict[f"block{blockNr}"]["condition"]
            trial     = blockDict[f"block{blockNr}"]["trial"]
                     
            rawBlock = RohBlock.erzeuge_gecroppteRaw_fuerBlock(rawFull, pathVMRK, blockLength, blockNr )
            raws_perFreqCombCond.append(rawBlock)
            freqCombCond_list.append(f"{freqComb}_{condition}")
            trial_list.append(f"trial{trial}")

            print("freqCombCond " + COLORYELLOW + f"{freqComb}_{condition} " + COLORRED + f"   block{blockNr}" + COLOREND)

        return raws_perFreqCombCond, freqCombCond_list, trial_list