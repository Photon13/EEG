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


class TestEpochs:

    @staticmethod
    def test_epochs():

        # TEILNEHMER DATEN:
        pNr = 2                        # <---
        durchgang = "2"                 # <---
            #default durchgang = ""

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
        #rawFull = mne.set_eeg_reference( rawFull, ref_channels = ["14"], verbose = True )[0]    # <---
        rawFull = rawFull.notch_filter(freqs = 50.0, notch_widths = 1.0)
        rawFull = rawFull.filter(l_freq = 1.0 , h_freq = 45.0 )


        """
        start, end = RohBlock.getBlockStartAndEnd( 8, rawFull.info["sfreq"], blockLength, pathVMRK )
        rawBlock_a = rawFull.copy().crop( tmin = start, tmax = end )

        start, end = RohBlock.getBlockStartAndEnd( 9, rawFull.info["sfreq"], blockLength, pathVMRK )
        rawBlock_b = rawFull.copy().crop( tmin = start, tmax = end )

        start, end = RohBlock.getBlockStartAndEnd( 10, rawFull.info["sfreq"], blockLength, pathVMRK )
        rawBlock_c = rawFull.copy().crop( tmin = start, tmax = end )

        start, end = RohBlock.getBlockStartAndEnd( 11, rawFull.info["sfreq"], blockLength, pathVMRK )
        rawBlock_d = rawFull.copy().crop( tmin = start, tmax = end )

        raw_concatenated4Blocks = mne.concatenate_raws([rawBlock_a, rawBlock_b, rawBlock_c, rawBlock_d], preload = True)


        #events = mne.make_fixed_length_events(raw_concatenated4Blocks, duration=0.1)
        events, event_id = mne.events_from_annotations(raw_concatenated4Blocks)
        event_id = {
            'S  2': 10001, 
            'S 32': 10002, 
            'S 34': 10003, 
            #'S128': 10004, 
            #'S161': 10005
        }
        

        epochs = mne.Epochs(
                            #raw_concatenated4Blocks, events=events, 
                            raw_concatenated4Blocks, events=events, event_id = event_id,
                            tmin = -0.5, tmax = 0.5, 
                            baseline = None, 
                            reject = None, reject_by_annotation = False,
                            preload = True, verbose = True) 
        epochs.plot_image(picks = ["13"])
        """

        events, event_id = mne.events_from_annotations(rawFull)
        event_id = {
            #'S  2': 10001, 
            #'S 32': 10002, 
            #'S 34': 10003, 
            #'S128': 10004, 
            'S161': 10005
        }
        

        epochs = mne.Epochs(
                            #raw_concatenated4Blocks, events=events, 
                            rawFull, events=events, event_id = event_id,
                            tmin = -0.5, tmax = 0.5, 
                            baseline = None, 
                            reject = None, reject_by_annotation = False,
                            preload = True, verbose = True) 
        epochs.plot_image()




TestEpochs.test_epochs()


