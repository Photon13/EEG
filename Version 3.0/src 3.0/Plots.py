import matplotlib.pyplot as plt
import numpy as np
import mne
from typing import List

from Ereignisse import Ereignisse

COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN = "\033[0;32m"
COLOREND = '\033[0m'


class Plots:

    @staticmethod
    def plotMarkers_perTime(rawFull, pathVMRK : str):
        events_tSampAbs, event_dict = Ereignisse.get_ereignisse(pathVMRK)
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
        events_tSampAbs, event_dict = Ereignisse.get_ereignisse(pathVMRK)

        reject_criteria = dict(          #?
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



    @staticmethod # self-made
    def plot_PSD(psds, freqs):
    
        fig,ax = plt.subplots( nrows=1 )

        plt.title("PSD spectrum", fontsize=20)
        plt.xlabel("Frequency [Hz]", fontsize=16)
        plt.ylabel("Power Spectral Density [uV^2/Hz?]", fontsize=16)

        # FULL VIEW:
        ax.set( xlim=(0, 60),   xticks=np.arange(start=0, stop=60, step=1.0)  )

        # DETAILED VIEW OF FREQ_RANGE:
        #ax.set( xlim=(30, 55),   xticks=np.arange(start=30, stop=55, step=0.5)  )
        #plt.xticks(fontsize = 7)

        ax.plot(freqs, psds)
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.show()
        inp = input("any ")



    @staticmethod # self_made
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
    def boxplot( data : dict, title : str, participantNr : int, ylabel : str, xlabel : str, axhline : float | None ) -> None:

        labels = data.keys()
        oldTicks = list( range(1, len(labels)+1 ) )

        boxes = []
        for label in labels:
            boxes.append( data[label] )

        plt.boxplot( 
            boxes,
            showmeans    = True,
            patch_artist = True,
            boxprops     = { "facecolor":"lightgrey" },
            medianprops  = { "color":"black" }, 
            meanprops    = { "marker":"s", "markerfacecolor":"white", "markeredgecolor":"black" },
            flierprops   = { "marker":"x" } #Outliers    
        )
        plt.title( f"{title}\n---Participant {participantNr}---", fontsize=13, fontweight='bold', pad=10 )
        #plt.rcParams["figure.figsize"] = (15,10)
        #plt.text( 2.1, 4.35, f"Participant {participantNr}", fontsize=12 )

        plt.ylabel( ylabel, fontsize=14 )
        plt.xlabel( xlabel, fontsize=12 )
        plt.xticks( oldTicks, labels )
        if( axhline != None ):
            plt.axhline(y = axhline, color = "grey", linestyle = ":")
        
        plt.tight_layout(pad=1)
        plt.show()
        inp = input("any ")
        plt.close()