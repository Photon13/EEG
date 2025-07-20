from BlockParams import BlockParams
from Ereignisse import Ereignisse

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

