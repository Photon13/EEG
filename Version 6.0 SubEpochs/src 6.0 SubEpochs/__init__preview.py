import mne 
import scipy
import copy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import os

from Ereignisse import Ereignisse
from BlockParams import BlockParams
from Plots import Plots

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'



def preview():

    blockNr = 68
    intervalNr = 1

    recordingElectrodes = ["25"]               # <---
    referenceElectrodes = ["15"]#["13", "15"]          # <---

    close_up = True  # <---
    save = False      # <---

    identifiers = [ 
        #[13, "3"],
        #[4, "4"],
        #[3, "3"],
        [2, "2"],
        #[1, "1"],
    ]

    folderName = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\bachelorThesisText\\RESULTS\\reinmüllOrdner"
    if( save == True ):  
        if( len( os.listdir(folderName) ) > 0 ):
            print( COLORRED + "CAVE: 'reinmüllOrdner' is not empty! " + COLOREND )
            while True:
                inp = input("Continue anyway? [yes]: ")
                if( inp.lower() == "yes" ):
                    break

    for idNr in range(len(identifiers)):
        pNr       = identifiers[idNr][0]
        durchgang = identifiers[idNr][1] 

        folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"
        file_id = f"participant{pNr}_mainExp{durchgang}"
        pathVHDR  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vhdr"
        pathVMRK  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vmrk"


        rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )


        bad_channels = []               
        for i in range(1, 64+1):
            bad_channels.append(str(i))

        used_channels = copy.deepcopy(recordingElectrodes)
        if( referenceElectrodes != None ):
            used_channels.extend(referenceElectrodes)
        for ch in used_channels :      # <---    
            bad_channels.remove(ch)  

        rawFull.drop_channels(bad_channels)


        if( referenceElectrodes != None ):
            rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]



        zBusses = Ereignisse.get_zBusse( pathVMRK )

        start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
        end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
        rawBlock  : object  = rawFull.copy().crop(tmin = start, tmax = end)

        voltage, times = mne.io.Raw.get_data(
            rawBlock,
            picks         = recordingElectrodes, 
            return_times  = True, 
            units         = "V",
        )
        voltage = voltage[0]

        start = 1 + int(rawFull.info["sfreq"]*intervalNr*5 )           # FIRSTMOST SAMPLE REMOVED (BECAUSE RAWBLOCK IS 15001 SAMPLES LONG)
        end   = start + 5000 # 10 sec

        voltage_interval = copy.deepcopy( voltage[start:end])

        freqs, psds = scipy.signal.periodogram(
            x       = voltage_interval,
            fs      = rawFull.info["sfreq"],
            scaling = "density" 
        )
        Plots.plot_PSD(
            psds, 
            freqs, 
            f"participant{pNr} block{blockNr}",
            intervalNr,
            recordingElectrodes,
            referenceElectrodes,
            folderName, 
            pNr, 
            close_up,   
            save
        )


preview()