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
from Elektroden import Elektroden
from Paths import Paths

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
        pNr = 13                        # <---
        durchgang = "3"                 # <---
            #default durchgang = ""

        # PFADE:
        pathVHDR, pathVMRK, pathBlockDict = Paths.get_paths(pNr, durchgang)

        # PARAMETER:
        blockLength  = BlockParams.BLOCK_LENGTH 
        n_blocks     = BlockParams.N_BLOCKS
        famA = BlockParams.FAM_A
        famB = BlockParams.FAM_B
        famC = BlockParams.FAM_C

        # ELEKTRODEN
        recE = Elektroden.RECORDING_ELECTRODE
        refE = Elektroden.REFERENCE_ELECTRODE


        ##############################################################################################################################################

        # LADE RAW FULL:
        rawFull = Roh.lade_fullRaw( pathVHDR )
        rawFull = Roh.assign_unusedChannels_asBads( rawFull )

        ##############################################################################################################################################

        # PLOTTE CHANNELS RAW_BLOCK:
        start, end = RohBlock.getBlockStartAndEnd( blockNr, rawFull.info["sfreq"], blockLength, pathVMRK )
        rawBlock = rawFull.copy().crop( tmin = start, tmax = end )

        
        rawBlock = mne.set_eeg_reference( 
            rawBlock, 
            ref_channels = {
                "14" : ["13", "15"]  # <---
            }, 
            verbose = True )[0]
        
        rawBlock.copy().pick_types( include = ["13", "14", "15"] ).plot( duration = 5.0 )  # <---
        inp = input("any")

        ##############################################################################################################################################

        # BERECHNE PSD_WERTE ALS ARRAY:
        psds, psds_dB, freqs  = Berechnungen.get_psds( rawBlock, blockLength )

        #Plots.plot_PSD(psds, freqs)            #un_normiert
        Plots.plot_PSD(psds_dB, freqs)          #un_normiert, dB

        ##############################################################################################################################################

        # BERECHNE PSD ÜBER MNE:
        mne.viz.plot_raw_psd(rawBlock, picks=["14"], xscale="linear", dB=True, estimate="power", fmin=25.0, fmax=60.0)
        inp = input("any")

        ##############################################################################################################################################




Main_singleBlock.main_singleBlock(1)













