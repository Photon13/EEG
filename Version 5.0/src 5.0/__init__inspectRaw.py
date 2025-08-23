import mne
import json
import copy
import numpy as np
from typing import List

from BlockParams import BlockParams
from Ereignisse import Ereignisse
from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'



# CHOOSE PARTICIPANT:
pNr = 1                     # <---            
durchgang = "1"             # <---      
###########################


# SET PATHS:
folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"

pathVHDR : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vhdr"
pathVMRK : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vmrk"
pathBlockDict = f"data\\blockDict\\participant{pNr}_blockDict.txt"

with open( pathBlockDict, "r" ) as f:
    blockDict : dict[dict] = json.load(f)
###########################





# LADE RAW FULL:
rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )
l_freq = 1.0
h_freq = 60.0
notch_freq = 50.0
notch_width = 1.0
rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )
###########################


# SET REFERENCE (OPTIONAL):
#rawFull = mne.set_eeg_reference( rawFull, ref_channels = ["13", "15"])[0]     # <---
###########################


# REMOVE INTERVALLS BETWEEN BLOCKS:
zBusses = Ereignisse.get_zBusse( pathVMRK )

allRaws : List[object] = []
for blockNr in range(72):
        start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
        end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
        rawBlock  : object  = rawFull.copy().crop(tmin = start, tmax = end)
        allRaws.append (rawBlock)

mne.concatenate_raws( allRaws )
allRaws = allRaws[0]
###########################


picks = ["14", "20", "25", "27", "13", "15"]

allRaws.plot(picks = picks) 
inp = input("any ")