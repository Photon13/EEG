# Solution for ICAParams must be found
# Tuple of args given to mne.preprocessing.ICA() ?


import mne
import json
import numpy as np
from typing import List
import copy
import matplotlib
matplotlib.use('TkAgg') #choose TkAgg backend to display graphics
import matplotlib.pyplot as plt
plt.ion() #enables interactive mode for pyplot


from Roh import Roh
from RohBlock import RohBlock
from Berechnungen import Berechnungen
from Konvertierung import Konvertierung
from Normierung import Normierung
from BlockParams import BlockParams
from Ereignisse import Ereignisse
import Matrices
from Plots import Plots
from Elektroden import Elektroden
from Paths import Paths
from AllResults import AllResults

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'






###########################

pNr = 2                        # <---
durchgang = "2"                # <---


recordingElectrodes = ["20", "25", "27"]
referenceElectrodes = ["20", "25", "27"]
picks = ["20", "25", "27"]

l_freq = 1.0
h_freq = 60.0
notch_freq = 50.0
notch_width = 1.0

n_componentsICA = 0.999
methodICA = 'fastica'
seed=99

n_fft = 65536
n_per_seg = 60000
n_overlap = 0
###########################








# PFADE:
pathAllResults = "data\\results\\allResults.pkl"

#allResults = list()
#AllResults.saveAsPickle_allResults(allResults, pathAllResults)

allResults = AllResults.loadFromPickle_allResults(pathAllResults)
print(allResults)

pathVHDR, pathVMRK, pathBlockDict = Paths.get_paths(pNr, durchgang)
with open( pathBlockDict, "r" ) as f:
    blockDict = json.load(f)

# PARAMETER:
blockLength  = BlockParams.BLOCK_LENGTH 
n_blocks     = BlockParams.N_BLOCKS
famA = BlockParams.FAM_A
famB = BlockParams.FAM_B
famC = BlockParams.FAM_C








##########################################################################################################################################



# LADE RAW FULL:
rawFull = Roh.lade_fullRaw( pathVHDR )



# ICA:
ica = mne.preprocessing.ICA(
    n_components = n_componentsICA, 
    method = methodICA, 
    random_state=seed
)
ica.fit(rawFull)  # bad segments that were marked in the EEG signal will be excluded.
ica.plot_sources(rawFull)
ica.apply(rawFull)



# FILTERING:
rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )

# RE_REFERENCING:
rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes, verbose = True )[0] 

# DISCARD CHANNELS NOT BEING RECORDING ELECTRODES:
allChannels = rawFull.info["ch_names"]
bad_channels = allChannels.copy()
for ch in recordingElectrodes: 
    bad_channels.remove(ch)
rawFull.drop_channels(bad_channels)


   

##########################################################################################################################################



zBusse : List[int] = Ereignisse.get_zBusse( pathVMRK )


# SORT BLOCKS:
# create dict:
bIndices_perFreqCombCond : dict[List[int]] = dict()
for freqComb in ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]:
    for condition in ["left", "middle", "right", "both"]:
        bIndices_perFreqCombCond[f"{freqComb}_{condition}"] = list()

# fill dict with proper blockIndices:
for i in range(72):
    freqComb  : str = blockDict[f"block{i}"]["freqComb"]
    condition : str = blockDict[f"block{i}"]["condition"]
    bIndices_perFreqCombCond[f"{freqComb}_{condition}"].append(i)

# COLLECT INDICES OF SIMILAR BLOCKS:
zBusse = Ereignisse.get_zBusse( pathVMRK )
croppedRaws : List[mne.io.Raw] = list()
for i in range(72):
    start, stop = RohBlock.getBlockStartAndEnd( i, rawFull.info["sfreq"], blockLength, pathVMRK )
    segment = RohBlock.erzeuge_gecroppteRaw_fuerBlock(rawFull, pathVMRK, blockLength, i )
    croppedRaws.append(segment)


# COLLECT RAWS OF SIMILAR BLOCKS:
raws_perFreqCombCond : dict[List[mne.io.Raw]] = copy.deepcopy( bIndices_perFreqCombCond )

for freqCombCond in bIndices_perFreqCombCond:
    indices : List[int] = bIndices_perFreqCombCond[freqCombCond]

    for j in range( len( indices) ): #default range(3)
        blockIndex : int = indices[j] 
        raws_perFreqCombCond[freqCombCond][j] = copy.deepcopy( croppedRaws[ blockIndex ] )



##########################################################################################################################################



for freqCombCond in raws_perFreqCombCond:
    rawList : List[mne.io.Raw] = raws_perFreqCombCond[freqCombCond] 
    rawConcat = mne.concatenate_raws(rawList)

    psds_arr, psds_dB_arr, freqs_arr, voltage_arr, times_arr = Berechnungen.get_multiplePsds( 
        rawConcat, 
        blockLength = blockLength,
        n_fft       = n_fft,
        n_per_seg   = n_per_seg,
        n_overlap   = n_overlap, 
        picks       = recordingElectrodes 
    )

    allResults = AllResults.appendResult_toAllResults(
        allResults          = allResults,                               
        file_id             = f"participant{pNr}_mainExp{durchgang}.vhdr",                                     
        freqCombCond        = freqCombCond,
        recordingElectrodes = recordingElectrodes,
        referenceElectrodes = referenceElectrodes, 
        filterParams        = (l_freq, h_freq, notch_freq, notch_width),
        ICAParams           = (n_componentsICA, methodICA, seed), #??????
        fourierParams       = (n_fft, n_per_seg, n_overlap), 
        voltageFreqs        = (voltage_arr, times_arr), 
        psdsFreqs           = (psds_arr, psds_dB_arr, freqs_arr)
    )
    AllResults.saveAsPickle_allResults( allResults, pathAllResults )

    print("Newly appended to allResults: " + COLORCYAN + f"{allResults[-1]}" + COLOREND)

    
