import matplotlib.pyplot as plt
import numpy as np
import mne
import typing

from Mne_EEGAnalyse import Mne_EEGAnalyse

COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN = "\033[0;32m"
COLOREND = '\033[0m'


class Plots:

    @staticmethod
    def plot_PSD(psd, freqs):
        
        fig,ax = plt.subplots( nrows=1 )

        x = freqs
        y = psd[0]
        y = 10*np.log10(y)

        plt.title("PSD spectrum", fontsize=20)
        plt.xlabel("Frequency [Hz]", fontsize=16)
        plt.ylabel("Power Spectral Density [dB]", fontsize=16)

        ax.set(xlim=(0, 60), 
            xticks=np.arange(start=0, stop=60, step=2),
            #ylim=(0, 8), 
            #yticks=np.arange(1, 8)
        )
        ax.plot(x,y)

        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.show()
        inp = input("any ")


    @staticmethod
    def plot_SNR(snr, freqs):

        fig,ax = plt.subplots( nrows=1 )

        x = freqs
        y = snr[0]
        #y = 10*np.log10(y)

        plt.title("Signal-to-Noise Ratio", fontsize=20)
        plt.xlabel("Frequency [Hz]", fontsize=16)
        plt.ylabel("SNR", fontsize=16)
        #plt.ylabel("SNR [dB]", fontsize=16)

        ax.set(xlim=(0, 60), 
            xticks=np.arange(start=0, stop=60, step=2),
            #ylim=(0, 8), 
            #yticks=np.arange(1, 8)
        )
        ax.plot(x,y)

        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.show()
        inp = input("any ")

    @staticmethod
    def plotMarkers_perTime(rawFull, pathVMRK : str):

        events_tSampAbs, event_dict = Mne_EEGAnalyse.get_events(pathVMRK)

        fig = mne.viz.plot_events( 
            events     = events_tSampAbs, 
            event_id   = event_dict, 
            sfreq      = rawFull.info["sfreq"], 
            first_samp = rawFull.first_samp
        )
        inp = input("Continue? [any]: ")


    @staticmethod
    def plot_evokedPotentials(anyRaw, pathVMRK, markerFullName : str):
        """ markerFullName E {zBus, button, shiftLeft, shiftMiddle, shiftRight} """

        events_tSampAbs, event_dict = Mne_EEGAnalyse.get_events(pathVMRK)

        reject_criteria = dict( #?
            eeg=150e-6,  # 150 µV
        )

        epochs = mne.Epochs(
            anyRaw,
            events = events_tSampAbs,
            event_id = event_dict,
            tmin = -0.2,
            tmax =  0.5,
            reject_by_annotation = True,
            #reject=reject_criteria,
            preload = True
        )
        aud_epochs = epochs[ markerFullName ]
        aud_epochs.plot_image(picks=["Cz"])
        inp = input("any ")