import mne
import json
import numpy as np
from typing import List

from Roh import Roh
from RohBlock import RohBlock
from Konvertierung import Konvertierung
import Matrices
from Berechnungen import Berechnungen

COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN = "\033[0;32m"
COLOREND = '\033[0m'


# TEILNEHMER DATEN
pNr = 0                 # <---

# PFADE:
pathCWD   = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder\\Version 3.0"
folderEEG = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"
pathVHDR = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp1.vhdr"
pathVMRK = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp1.vmrk"
pathBlockDict = ""

# LADE RAW:
rawFull = Roh.lade_fullRaw( pathVHDR )
rawFull = Roh.renameChannels( rawFull )
rawFull = Roh.assign_unusedChannels_asBads( rawFull )
rawFull.notch_filter( rawFull, Fs = rawFull.info["sfreq"], freqs = 50.0, notch_widths = 10 )

# ERZEUGE RAW FÜR BESTIMMTEN BLOCK:
blockNr = 0                                                         # <---
start, end = RohBlock.getBlockStartAndEnd( blockNr, pathVMRK )
rawBlock = rawFull.copy().crop( tmin = start, tmax = end )

# ABRUF BLOCK-DATEN
with open( pathBlockDict, "r" ) as f:
    blockDict = json.load(f)

freqComb  = blockDict[f"block{blockNr}"]["freqComb"]
target    = blockDict[f"block{blockNr}"]["condition"]


##############################################################################################################################################


# BERECHNE POWER für famA, famB und famC:
P_fABC : List[float] = Berechnungen.berechnePower_P_fABC( rawBlock )

# KONVERTIERE P_fABC ZU P_fLMR:
P_fLMR : List[float] = Konvertierung.get_P_fLMR( freqComb, P_fABC )

# BESTIMME P_fTarget:
P_fTarget : float = Berechnungen.bestimme_P_fTarget( P_fLMR, target )

# BESTIMME P_fNonTarget:
P_fNonTarget : float = Berechnungen.bestimme_P_fNonTarget( P_fLMR, target )

# PRINT RESULTS:
print( "P_fABC = " + COLORCYAN + f"{P_fABC}" + COLOREND )
print( "P_fLMR = " + COLORCYAN + f"{P_fLMR}" + COLOREND )
print( "P_fTarget = " + COLORCYAN + f"{P_fTarget}" + COLOREND )
print( "P_fNonTarget = " + COLORCYAN + f"{P_fNonTarget}" + COLOREND )


##############################################################################################################################################




