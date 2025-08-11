import matplotlib.pyplot as plt
import numpy as np
import mne
from typing import List
import seaborn as sns

from Ereignisse import Ereignisse
from BlockParams import BlockParams

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



    @staticmethod
    def plot_PSD( avg_pows, freqs, freqCombCond, folderName, pNr, close_up : bool, save : bool ):
        plt.figure( figsize=(10, 5) )
        plt.plot(   freqs, avg_pows, label="", color = "black" )

        for fam in BlockParams.FAMS_ABC:
            plt.axvline( fam, color='grey', linestyle=':', alpha=0.8, linewidth=3.0, zorder=0 ) # Vertical lines

        plt.title(f"{freqCombCond}", fontsize=16, fontweight='bold', pad=20 )
        plt.xlabel("$f$ [$Hz$]", fontsize=14)
        plt.ylabel(r"$PSD$ [$\frac{V^{2}}{Hz}$]", fontsize=14) 


        if( close_up == False ):
            min_f, max_f, step = 0.0, 60.0, 5.0

        elif( close_up == True ):
            min_f, max_f, step = 35.0, 45.0, 1.0
            plt.ylim( bottom = -1e-13, top = 1.5*1e-11  )


        plt.xlim( min_f, max_f )
        plt.xticks( np.arange(min_f, max_f+1, step), fontsize=12 )
        plt.yticks(fontsize=14)

        #plt.grid(True)
        plt.tight_layout() 
        plt.show()

        if( save == True ):
            fileName = folderName + f"\\psd_{freqCombCond}_participant{pNr}.png"
            plt.savefig(fname = fileName)
        elif( save == False ):
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
        plt.title( f"{title}\n---Participant {participantNr}---", fontsize=16, fontweight='bold', pad=10 )
        #plt.rcParams["figure.figsize"] = (15,10)
        #plt.text( 2.1, 4.35, f"Participant {participantNr}", fontsize=12 )

        plt.ylabel( ylabel, fontsize=14 )
        plt.xlabel( xlabel, fontsize=14 )
        plt.xticks( oldTicks, labels, fontsize = 14 )
        plt.yticks( fontsize = 14)
        if( axhline != None ):
            plt.axhline(y = axhline, color = "grey", linestyle = ":")
        
        plt.tight_layout(pad=1)
        plt.show()
        inp = input("any ")
        plt.close()

