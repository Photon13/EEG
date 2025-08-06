# Solution for ICAParams must be found
# Tuple of args given to mne.preprocessing.ICA() ?


import mne
import json
from typing import List


from Roh import Roh
from RohBlock import RohBlock
from BlockParams import BlockParams
from Paths import Paths
from AllResults import AllResults

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'






###########################         # <---

pNr = 2                        
durchgang = "2"                


recordingElectrodes = ["14", "20", "25", "27"]
referenceElectrodes = ["13"]
picks = ["20", "25", "27", "13"]

l_freq = 1.0
h_freq = 60.0
notch_freq = 50.0
notch_width = 1.0

n_componentsICA = None #0.999
methodICA = None #'fastica'
seed= None #99

voltageUnit = "V"

n_fft = 65536
n_per_seg = 60000
n_overlap = 0
###########################




###########################           # <---
# PFADE:
pathAllResults = "data\\results\\allResultsVolt_testPSDUnits.pkl"

#AllResults.create_newAllResultsList( pathAllResults )

allResultsVolt = AllResults.loadFromPickle_allResults(pathAllResults)
###########################



pathVHDR, pathVMRK, pathBlockDict = Paths.get_paths(pNr, durchgang)
with open( pathBlockDict, "r" ) as f:
    blockDict = json.load(f)

# PARAMETER:
blockLength  = BlockParams.BLOCK_LENGTH 
n_blocks     = BlockParams.N_BLOCKS
famA = BlockParams.FAM_A
famB = BlockParams.FAM_B
famC = BlockParams.FAM_C


# LADE RAW FULL:
rawFull = Roh.lade_fullRaw( pathVHDR )






###########################         # <---
# ICA:
"""
ica = mne.preprocessing.ICA(
    n_components = n_componentsICA, 
    method = methodICA, 
    random_state=seed
)
ica.fit(rawFull)  # bad segments that were marked in the EEG signal will be excluded.
ica.plot_sources(rawFull)
ica.apply(rawFull)
"""

# FILTERING:
rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )
###########################







# RE_REFERENCING:
rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes, verbose = True )[0] 


# DISCARD CHANNELS NOT BEING RECORDING ELECTRODES:
allChannels = rawFull.info["ch_names"]
bad_channels = allChannels.copy()
for ch in recordingElectrodes: 
    bad_channels.remove(ch)
rawFull.drop_channels(bad_channels)


   




raws_perFreqCombCond = RohBlock.get_rawsPerFreqCombCond( rawFull, pathVMRK, blockDict, blockLength )

for freqCombCond in raws_perFreqCombCond: #key = freqCombCond
    rawConcat = mne.concatenate_raws( raws_perFreqCombCond[freqCombCond] )

    voltage, times = mne.io.Raw.get_data(
            rawConcat,
            picks         = recordingElectrodes, 
            return_times  = True, 
            units         = voltageUnit,
            verbose       = True
    )
    
    paramDict = {                                                 
        "file_id"             : f"participant{pNr}_mainExp{durchgang}.vhdr",                                   
        "freqCombCond"        : freqCombCond,
 
        "recordingElectrodes" : recordingElectrodes,
        "referenceElectrodes" : referenceElectrodes,

        "sfreq"                : rawConcat.info["sfreq"],

        "filterParams"        : (l_freq, h_freq, notch_freq, notch_width),
        "ICAParams"           : (n_componentsICA, methodICA, seed),

        "voltageUnit"         : voltageUnit,
        "voltageTimes"        : (voltage, times)
    }
    
    allResultsVolt.append(paramDict)
    AllResults.saveAsPickle_allResults( allResultsVolt, pathAllResults )

    print("Newly appended to allResults: " + COLORCYAN + f"{allResultsVolt[-1]}" + COLOREND)
    #AllResults.showAllResults( allResultsVolt )

    
