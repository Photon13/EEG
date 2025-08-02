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



##########################################################################################################################################



# TEILNEHMER DATEN:
pNr = 2                        # <---
durchgang = "2"                 # <---
    #default durchgang = ""

# pnr=2 durchgang=2
# pnr=13 durchgang=3


# PFADE:
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
ica = mne.preprocessing.ICA(n_components=0.999, method='fastica', random_state=99)
ica.fit(rawFull)  # bad segments that were marked in the EEG signal will be excluded.
#ica.plot_sources(rawFull)
ica.apply(rawFull)



# FILTERING:
rawFull = rawFull.notch_filter(freqs = 50.0, notch_widths = 1.0)
rawFull = rawFull.filter(l_freq=1, h_freq=60)



# DISCARD CHANNELS NOT BEING PICKS:
allChannels = rawFull.info["ch_names"]
picks = ['20', '25', '27', '13', '15']                 #### <----- 
# ["13", "15", "14", "20", "25", "27"]


bad_channels = allChannels.copy()
for ch in picks: 
    bad_channels.remove(ch)
rawFull.drop_channels(bad_channels)




# RE_REFERENCING:
reference = "average"         #### <----- 

rawFull = mne.set_eeg_reference( rawFull, ref_channels = reference, verbose = True )[0]    



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

    """
    psds = rawConcat.compute_psd(
        method='welch',
        picks = ["13", "15"], #### <----- 
        fmin=30, fmax=55,
        n_per_seg=2000,
        n_overlap=1000,
        verbose=True
    )

    # Convert to dB
    psds_db = 10 * np.log10(psds.get_data())  # shape: (n_channels, n_freqs)
    freqs = psds.freqs
    """

    psds_arr, psds_dB_arr, freqs_arr = Berechnungen.get_multiplePsds( 
        rawConcat, 
        blockLength,
        n_fft = 65536,
        n_per_seg = 60000,
        n_overlap = 0, 
        picks = ['20', '25', '27', '13', '15'] )        #### <----
    
    # === Average PSD across channels ===
    psds = psds_dB_arr.mean(axis=0)

  

    ##########################################################################################################################################



    plt.figure(figsize=(10, 5))
    plt.plot(freqs_arr[0], psds, label="Average PSD (across channels)")         #### <-----

    for tf in [35.9, 39.7, 43.2]:
        plt.axvline(tf, color='red', linestyle='--', alpha=0.8, linewidth=1.2) # Vertical lines

    plt.title(f"PSD of Concatenated Blocks ({freqCombCond})")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power Spectral Density [dB]")
    plt.xlim(34, 45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()


    plt.savefig(fname = f"plots\\PSD_concatBlocks_{freqCombCond}_picks_{picks}_ref_{reference}")



    ##########################################################################################################################################