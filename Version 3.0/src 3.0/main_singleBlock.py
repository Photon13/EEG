import mne
import json
import numpy as np
from typing import List

from Roh import Roh
from RohBlock import RohBlock
from Berechnungen import Berechnungen
from Konvertierung import Konvertierung
from Normierung import Normierung
from BlockParams import BlockParams
import Matrices
from Plots import Plots

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLOREND    = '\033[0m'

@staticmethod
def main_singleBlock(blockNr):

    # TEILNEHMER DATEN:
    pNr = 0                 # <---

    blockLength  = BlockParams.BLOCK_LENGTH 
    n_blocks     = BlockParams.N_BLOCKS
    famA = BlockParams.FAM_A
    famB = BlockParams.FAM_B
    famC = BlockParams.FAM_C


    # PFADE:
    pathCWD   = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder\\Version 3.0"
    folderEEG = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"
    pathVHDR  = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp1.vhdr"
    pathVMRK  = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp1.vmrk"
    pathBlockDict = f"data\\blockDict\\participant{pNr}_blockDict.txt"

    # LADE RAW:
    rawFull = Roh.lade_fullRaw( pathVHDR )
    rawFull = Roh.renameChannels( rawFull )
    rawFull = Roh.assign_unusedChannels_asBads( rawFull )
    #rawFull.notch_filter( rawFull, freqs = 50.0, notch_widths = 10 )

    ##############################################################################################################################################

    # BESTIMME NORMIERUNGS-DIVIDENT:
    #   (muss nur einmal pro Teilnehmer durchgeführt werden)
    #   WERT DANN IN CLASS NORMIERUNG EINFÜGEN
    """
    normierungsDivident = Normierung.get_NormierungsDivident(rawFull, pathVMRK, n_blocks, blockLength)
    print("normierungsDivident = " + COLORYELLOW + f"{normierungsDivident}" + COLOREND)
    """
    # <- Breakpoint hierher
    normierungsDivident = Normierung.NormierungsDivident[pNr]

    ##############################################################################################################################################

    # ERZEUGE RAW FÜR BESTIMMTEN BLOCK:
    start, end = RohBlock.getBlockStartAndEnd( blockNr, rawFull.info["sfreq"], blockLength, pathVMRK )
    rawBlock = rawFull.copy().crop( tmin = start, tmax = end )

    # ABRUF BLOCK-DATEN:
    with open( pathBlockDict, "r" ) as f:
        blockDict = json.load(f)

    freqComb  = blockDict[f"block{blockNr}"]["freqComb"]
    target    = blockDict[f"block{blockNr}"]["condition"]

    # BERECHNE PSD_WERTE FÜR SPEZIFIZIERTEN BLOCK:
    psds, psds_dB, freqs  = Berechnungen.get_psds( rawBlock, blockLength )
    psds_normiert         = Normierung.normiere_psds_dB( psds_dB, normierungsDivident )

    P_fABC_normiert       = Berechnungen.berechnePower_P_fABC( [famA, famB, famC], freqs, psds_normiert )
    P_fLMR_normiert       = Berechnungen.bestimme_P_fLMR( freqComb, P_fABC_normiert )
    P_fTarget_normiert    = Berechnungen.bestimme_P_fTarget( P_fLMR_normiert, target )
    P_fNonTarget_normiert = Berechnungen.bestimme_P_fNonTarget( P_fLMR_normiert, target )

    print( f"P_fABC_normiert_BLOCK{blockNr} = "       + COLORCYAN  + f"{P_fABC_normiert}"       + COLOREND )
    print( f"P_fLMR_normiert_BLOCK{blockNr} = "       + COLORCYAN  + f"{P_fLMR_normiert}"       + COLOREND )
    print( f"P_fTarget_normiert_BLOCK{blockNr} = "    + COLORCYAN  + f"{P_fTarget_normiert}"    + COLOREND )
    print( f"P_fNonTarget_normiert_BLOCK{blockNr} = " + COLORCYAN  + f"{P_fNonTarget_normiert}" + COLOREND )

    ##############################################################################################################################################

    # PLOT PSD FÜR BLOCK:
    #Plots.plot_PSD(psds, freqs)            #un_normiert
    #Plots.plot_PSD(psds_dB, freqs)         #un_normiert, dB
    #Plots.plot_PSD(psds_normiert, freqs)   #normiert (psd < 1: unterdurchschnittlich, psd>1: durchschnittlich)


    return psds_normiert, freqs, P_fABC_normiert, P_fLMR_normiert, P_fTarget_normiert, P_fNonTarget_normiert












