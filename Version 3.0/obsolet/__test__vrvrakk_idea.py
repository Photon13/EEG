import mne
import json
import numpy as np
from typing import List
import matplotlib.pyplot as plt

from Roh import Roh
from RohBlock import RohBlock
from Berechnungen import Berechnungen
from Konvertierung import Konvertierung
from Normierung import Normierung
from BlockParams import BlockParams
import Matrices
from Plots import Plots
from Elektroden import Elektroden
from Paths import Paths




# TEILNEHMER DATEN:
pNr = 2                        # <---
durchgang = "2"                 # <---
    #default durchgang = ""

#2 pnr
#2 durchgang
#10 block

#13 pnr
#3 durchgang

# PFADE:
pathVHDR, pathVMRK, pathBlockDict = Paths.get_paths(pNr, durchgang)


# PARAMETER:
blockLength  = BlockParams.BLOCK_LENGTH 
n_blocks     = BlockParams.N_BLOCKS
famA = BlockParams.FAM_A
famB = BlockParams.FAM_B
famC = BlockParams.FAM_C




# LADE RAW FULL:
rawFull = Roh.lade_fullRaw( pathVHDR )

rawFull = mne.set_eeg_reference( rawFull, ref_channels = "average", verbose = True )[0]    # <---
rawFull = rawFull.notch_filter(freqs = 50.0, notch_widths = 1.0)







start, end = RohBlock.getBlockStartAndEnd( 10, rawFull.info["sfreq"], blockLength, pathVMRK )
rawBlock_a = rawFull.copy().crop( tmin = start, tmax = end )

start, end = RohBlock.getBlockStartAndEnd( 31, rawFull.info["sfreq"], blockLength, pathVMRK )
rawBlock_b = rawFull.copy().crop( tmin = start, tmax = end )

start, end = RohBlock.getBlockStartAndEnd( 66, rawFull.info["sfreq"], blockLength, pathVMRK )
rawBlock_c = rawFull.copy().crop( tmin = start, tmax = end )

rawConcat = mne.concatenate_raws([rawBlock_a, rawBlock_b, rawBlock_c])
rawConcat.plot(duration = 5.0)



