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
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


class Main_singleBlock:

    @staticmethod
    def main_singleBlock(blockNr):

        # TEILNEHMER DATEN:
        pNr = 13                 # <---

        blockLength  = BlockParams.BLOCK_LENGTH 
        n_blocks     = BlockParams.N_BLOCKS
        famA = BlockParams.FAM_A
        famB = BlockParams.FAM_B
        famC = BlockParams.FAM_C


        # PFADE:
        pathCWD   = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder\\Version 3.0"
        folderEEG = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"
        pathVHDR  = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp3.vhdr"
        pathVMRK  = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp3.vmrk"
        pathBlockDict = f"data\\blockDict\\participant{pNr}_blockDict.txt"

        # LADE RAW:
        rawFull = Roh.lade_fullRaw( pathVHDR )
        rawFull = Roh.renameChannels( rawFull )
        rawFull = Roh.assign_unusedChannels_asBads( rawFull )
        rawFull = Roh.changeReference_toAverageAuricles(rawFull)
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
        normierungsDivident = Normierung.NormierungsDivident[f"participant{pNr}"]

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

        ##############################################################################################################################################

        # PLOT rawBlock:
        #rawFull.plot()
        #rawBlock.plot()
        #inp = input("any")
        # 
        #  PLOT PSD FÜR BLOCK:
        #Plots.plot_PSD(psds, freqs)            #un_normiert
        #Plots.plot_PSD(psds_dB, freqs)          #un_normiert, dB
        #Plots.plot_PSD(psds_normiert, freqs)   #normiert (psd < 1: unterdurchschnittlich, psd>1: durchschnittlich)

        return psds, psds_dB, psds_normiert, freqs, blockDict


Main_singleBlock.main_singleBlock(2)











