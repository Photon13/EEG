from typing import List
import mne
import pickle

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

import numpy as np
import scipy.signal
import sys

from AllResults import AllResults

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


def psdArrayWelch(voltage : np.ndarray, sfreq : int ):
    pows, freqs = mne.time_frequency.psd_array_welch(
        x         = voltage,
        sfreq     = sfreq,
        n_fft     = 131072,
        n_per_seg = 5000,
        n_overlap = 2500,
        average   = "mean"
    )
    #psds_db = 10 * np.log10(psds)
    return pows, freqs


def scipyPowerSpectrum(voltage : np.ndarray, sfreq : int ):
    freqs, pows = scipy.signal.periodogram(
        x       = voltage,
        fs      = sfreq,
        nfft    = 131072,
        scaling = "density" #
    )
    return pows, freqs


def calcAverage( pows : List[np.ndarray] | np.ndarray ):
    if( type(pows) == List or list ):
        pows = np.array(pows)

    if( pows.ndim == 2 ):
        # === Average PSD across channels ===
        avg_pows = pows.mean(axis=0)
    else:
        avg_pows = pows
    return avg_pows



def plotting(avg_pows, freqs, freqCombCond):
    plt.figure( figsize=(10, 5) )
    plt.plot(   freqs, avg_pows, label="" )

    for fam in [35.9, 39.7, 43.2]:
        plt.axvline( fam, color='red', linestyle='--', alpha=0.8, linewidth=1.2 ) # Vertical lines

    plt.title(f"{freqCombCond}")
    plt.xlabel("$f$ [$Hz$]")
    plt.ylabel(r"$PSD$ [$\frac{V^{2}}{Hz}$]") ####

    #min_f = 0.0
    #max_f = 60.0
    #step  = 5.0

    min_f = 34.0
    max_f = 45.0
    step  = 1.0

    plt.xlim(min_f, max_f) #(34, 45)
    plt.xticks( np.arange(min_f, max_f+1, step) )


    plt.grid(True)
    plt.legend() #?
    plt.tight_layout() #?
    plt.show()

    #plt.savefig(fname = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\plots\participant2\\PSD_concatBlocks_{target_group}_picks_{picks}_ref_{reference}")
    plt.show()
    inp = input("any ")






pathAllResults = "data\\results\\allResultsVolt_testPSDUnits.pkl"

criteria = {
    "file_id"             : 'participant2_mainExp2.vhdr',
    "freqCombCond"        : "ABC_both",
    "recordingElectrodes" : ["14", "20", "25", "27"],
    "referenceElectrodes" : ["13"]
}
with open(pathAllResults, "rb") as f:
    allResults = pickle.load(f)

idx_propEntr = AllResults.getIndices_ofEntriesMatchingCriteria( allResults, criteria )

#########
index = 3   # <---
#########
print(allResults[index])




voltage             = allResults[index]["voltageTimes"][0]
times               = allResults[index]["voltageTimes"][1]
freqCombCond        = allResults[index]["freqCombCond"]
sfreq               = allResults[index]["sfreq"]
recordingElectrodes = allResults[index]["recordingElectrodes"]





# SCI-PY:
pow_list = list()

for r in range( len(recordingElectrodes) ):
    pows, freqs  = scipyPowerSpectrum( voltage[r], sfreq )
    pow_list.append(pows)
avg_pows      = calcAverage( pow_list ) #does nothing if 1-dim array or list with 1 entry is given
plotting(avg_pows, freqs, freqCombCond)


# PSD und Power plot (scaling = "desnity" VS "spectrum") sind ebnahme identisch
# Werte bei niedrigen freqs um ca 0.5 y-Achsen Einheiten verschoben







"""
# MNE PSD ARRAY WELCH:
pow_list = list()
for r in range( len(recordingElectrodes) ):
    pows, freqs  = psdArrayWelch( voltage[r], sfreq )
    pow_list.append(pows)

avg_pows      = calcAverage( pow_list ) #does nothing if 1-dim array or list with 1 entry is given
plotting(avg_pows, freqs, freqCombCond)
"""





