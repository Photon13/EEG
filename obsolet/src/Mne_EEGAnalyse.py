import mne
import numpy as np

from typing import List
import re

COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN = "\033[0;32m"
COLOREND = '\033[0m'


class Mne_EEGAnalyse:


    @staticmethod
    def renameChannels(raw):

        #     Position     |  Elektrode    |  BVR Channel
        #__________________|_______________|_______________
        #    leftEar(A1)   |    13 grün    |      C3
        #    vertex(Cz)    |    14 grün    |      Cz
        #    rightEar(A2)  |    15 grün    |      C4

        mapping : dict = {              # old Channel name : new Channel name
            "C3"  :  "A1",
            "Cz"  :  "Cz",
            "C4"  :  "A2",
        }
        raw.rename_channels( 
            mapping = mapping,
            verbose = True
        )
        return raw
    
    @staticmethod
    def assign_unusedChannels_asBads(raw):
        picks = ["A1", "Cz", "A2"]      # Channels to keep
        bads = raw.ch_names.copy()
        for ch in picks:
            bads.remove(ch)
        raw.info["bads"].extend(bads)   # All other channels assigned as bads
        return raw
    
    @staticmethod
    def applyFilters(raw, l_freq : float = None, h_freq : float = None, notch : float = None):
        """ Eingabe eines floats oder ints bei einem Filtertyp führt zu dessen Anwendung.
            Anwendung mehrere Filtertypen gleichzeitig is möglich. """
        raw.filter( h_freq=h_freq, l_freq=l_freq)
        if( notch != None):
            raw.notch_filter(notch, notch_widths = 10)
        return raw
    
    @staticmethod
    def changeReference_toAverageAuricles(raw):
        refDict : dict = {
            "Cz" : ["A1","A2"]
        }
        raw = mne.set_eeg_reference(    # Replace Channel Cz with Cz - mean(A1,A2)
            raw, 
            ref_channels = refDict, 
            verbose = True 
        )[0]
        return raw

   
####################
    @staticmethod
    def get_raw(pathVHDR : str, renamedChannels : bool = True, reReferencing : bool = True, filtering : bool = False ):

        raw = mne.io.read_raw_brainvision(      # Load Header BVR file
            vhdr_fname = pathVHDR,
            ignore_marker_types = True, 
            preload = True,
            verbose = True 
        )
        ###
        if( renamedChannels == True ):
            raw = Mne_EEGAnalyse.renameChannels(raw)
        if( reReferencing == True ):
            raw = Mne_EEGAnalyse.changeReference_toAverageAuricles(raw)

        raw = Mne_EEGAnalyse.assign_unusedChannels_asBads(raw)

        if( filtering == True ):
            raw = Mne_EEGAnalyse.applyFilters(raw, l_freq = 1.0, h_freq = 60.0, notch = 50.0) 

        return raw
####################


    @staticmethod
    def get_events(pathVMRK : str):
        """ Extrahiert aus dem VMRK File die Marker-Ereignisse
            und generiert einen 3-dimensionalen npArray der Form [ [tSampAbs 0 markerNr] [...] ]. """
        with open( pathVMRK, "r" ) as f:
            lines = f.readlines()
        for i in range(0,12):
            lines.pop(0)

        events_tSampAbs : List[List] = []

        for l in lines:
            absTime = int( re.findall( r"\d+", l )[2] )
            markerNr = int( re.findall(r"\d+", l )[1] )
            newEntry = np.array([absTime, 0, markerNr])
            events_tSampAbs.append(newEntry)

        events_tSampAbs = np.array(events_tSampAbs) # 3-dimensional array:   e.g. [ [10784 0 161] [11345 0 32] ... ]

        event_dict = {
            "zBus" : 161,
            "shiftLeft" : 32,
            #"shiftMiddle" : 2,         # not existent for participant0
            "shiftRight" : 34,
            "button" : 128
        }

        print(COLORRED + "S  2 currently not used!. Remember to enable it in plotMarkers_perTime()." + COLOREND)
        return events_tSampAbs, event_dict


    @staticmethod
    def get_blockGrenzen_sortiertNachTarget(raw, events_tSampAbs, targetListe : List[str], blockDuration : int):
        """ returns:
                blockStartEnde_perTarget: dict = {
                    "left" : [ [23.33, 119.33], [...], ...],
                    ...
                    "both" : [ [2275.75, 2371.75], [...], ...]
                },
                blockIndices_perTarget : dict = {
                    "left" : [1,4,7,12],
                    ...
                    "both" : [5, 13, 17, 18]
                }, 
                zBusses : List[int] = [11889, ...] """

        blockIndices_perTarget : dict = {
            "left"   : list(),
            "middle" : list(),
            "right"  : list(),
            "both"   : list()
        }
        for i in range( len(targetListe) ):
            blockIndices_perTarget[ targetListe[i] ].append(i)

        ###

        zBusses : List[int] = []                                        # List containing time points for zBus markers
        for i in range( len(events_tSampAbs) ):             
            if( events_tSampAbs[i][2] == 161 ):
                zBusses.append( events_tSampAbs[i][0] )

        ###

        blockStartEnde_perTarget : dict = {
            "left"   : list(),
            "middle" : list(),
            "right"  : list(),
            "both"   : list()
        }

        for target in ["left", "middle", "right", "both"]:
            for blockIndex in blockIndices_perTarget[target]:
                start = zBusses[blockIndex]                # Block-Start in Samples  (absolut)
                start = float(start) / raw.info["sfreq"]   # Block-Start in Sekunden (absolut)
                ende = start + blockDuration               # Block-Ende  in Sekunden (absolut)

                blockStartEnde_perTarget[target].append( [start, ende] )
                
        return blockStartEnde_perTarget, blockIndices_perTarget, zBusses


    @staticmethod
    def concatenate_raws(raw, target : str, blockStartEnde_perTarget : dict):
        rawList = []
        for block in blockStartEnde_perTarget[target]:
            raw_cropped = raw.copy().crop( block[0], block[1] ) 
            rawList.append(raw_cropped)
        mne.concatenate_raws(rawList)           # modfies first entry in rawList
        raws_concatenated = rawList[0].copy()

        return raws_concatenated
 

####################
    @staticmethod  
    def get_croppedRaw(pathVHDR : str, pathVMRK : str, targetList : List[str], blockDuration : int, target : str = None, renamedChannels : bool = True, reReferencing : bool = True, filtering : bool = False):
        
        raw = Mne_EEGAnalyse.get_raw(
            pathVHDR, 
            renamedChannels, 
            reReferencing, 
            filtering
        )
        events_tSampAbs, event_dict = Mne_EEGAnalyse.get_events( pathVMRK )
        blockStartEnde_perTarget, blockIndices_perTarget, zBusses = Mne_EEGAnalyse.get_blockGrenzen_sortiertNachTarget(
            raw, 
            events_tSampAbs, 
            targetList, 
            blockDuration
        )
        raws_concatenated = Mne_EEGAnalyse.concatenate_raws(
            raw, 
            target, 
            blockStartEnde_perTarget
        )
        return raws_concatenated       
####################




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


"""

spectrum = raws_concatenatedMiddle.compute_psd( 
    "welch",
    #fmin=fmin,
    #fmax=fmax,
    picks = "Cz",
    reject_by_annotation = True,
    verbose=True,
)
#spectrum.plot()
#inp = input("any ")

psd, freqs = spectrum.get_data(return_freqs=True)
# psd = [[V1 V2 ... Vn]]
# freqs = [f1 f2 ... fn]
# len( psd[0] ) == len( freqs )








epochs = mne.Epochs(
    raw,
    event_id="S161",
    tmin=tmin,
    tmax=tmax,
    baseline=None,
    verbose=False,
)

spectrum = epochs.compute_psd(
    "welch",
    n_fft=int(sfreq * (tmax - tmin)),
    n_overlap=0,
    n_per_seg=None,
    tmin=tmin,
    tmax=tmax,
    picks = "Cz",
    fmin=fmin,
    fmax=fmax,
    window="boxcar",
    verbose=True,
)

psds, freqs = spectrum.get_data(return_freqs=True) #retruns array, array
# psds : array = [ [[5.79597081e-41 ... 1.83861893e-10]]  [[1.62500339e-40 ... 3.46050230e-11]]  ...   [[1.78680039e-41 ... 3.65014037e-12]] ]
# freqs : array = [0.00000000e+00 1.04166667e-02 2.08333333e-02 ... 5.99791667e+01 5.99895833e+01 6.00000000e+01]

snrs = Mne_EEGAnalyse.snr_spectrum(psds, noise_n_neighbor_freqs=10, noise_skip_neighbor_freqs=1) 
print(snrs)
#snrs : array = [ [[nan nan nan ... nan nan nan]] [[nan nan nan ... nan nan nan]] ]


import matplotlib.pyplot as plt


fig, axes = plt.subplots(2, 1, sharex="all", sharey="none", figsize=(8, 5))
freq_range = range( np.where(np.floor(freqs) == 1.0)[0][0] , np.where(np.ceil(freqs) == fmax - 1)[0][0])

psds_plot = 10 * np.log10(psds) #V

# PSD

psds_mean = psds_plot.mean(axis=(0, 1))[freq_range]
axes[0].plot(freqs[freq_range], psds_mean, color="b") # x, y, colour

#psds_std = psds_plot.std(axis=(0, 1))[freq_range]
#axes[0].fill_between( freqs[freq_range], psds_mean - psds_std, psds_mean + psds_std, color="b", alpha=0.2)

axes[0].set(
    title="PSD spectrum", 
    ylabel="Power Spectral Density [dB]",
    xlim=[30, 35],
)


fig.show()
#raw.plot_psd( method = "welch", fmin = 30 , fmax = 35 , picks = ["Cz"]) #?
raw.compute_psd( method = "welch", fmin = 30, fmax = 35, picks = ["Cz"]).plot()
#inp = input("any ")



#########


# SNR spectrum
snr_mean = snrs.mean(axis=(0, 1))[freq_range]
axes[1].plot(freqs[freq_range], snr_mean, color="r")

#snr_std = snrs.std(axis=(0, 1))[freq_range]
#axes[1].fill_between(freqs[freq_range], snr_mean - snr_std, snr_mean + snr_std, color="r", alpha=0.2)

axes[1].set(
    title="SNR spectrum",
    xlabel="Frequency [Hz]",
    ylabel="SNR",
    ylim=[-2, 30],
    xlim=[30, 35],
)

##

"""

