from BlockParams import BlockParams
from Ereignisse import Ereignisse

class RohBlock:

    @staticmethod
    def getBlockStartAndEnd( blockNr, samplerate, pathVMRK ):

        zBusses = Ereignisse.get_zBusse( pathVMRK )

        start = float( zBusses[ blockNr ] ) / float( samplerate )
        end = start + BlockParams.BLOCK_LENGTH

        return start, end
