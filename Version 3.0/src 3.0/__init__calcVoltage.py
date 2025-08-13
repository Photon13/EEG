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

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'





# CHOOSE PARTICIPANT:
pNr = 4                  # <---            
durchgang = "4"          # <---      
###########################






# PARAMETER:
blockLength  = BlockParams.BLOCK_LENGTH 
n_blocks     = BlockParams.N_BLOCKS
famA = BlockParams.FAM_A
famB = BlockParams.FAM_B
famC = BlockParams.FAM_C
###########################




# SET PATHS:
pathVHDR, pathVMRK, pathBlockDict = Paths.get_paths(pNr, durchgang)
with open( pathBlockDict, "r" ) as f:
    blockDict = json.load(f)



###########################





# LADE RAW FULL:
rawFull = Roh.lade_fullRaw( pathVHDR )
#rawFull.plot()                                 # <---
###########################
#  DROP BAD CHANNELS:
bad_channels = []
for i in range(1, 64+1):
    bad_channels.append(str(i))

for ch in ["25", "13", "15"] :      # <---    
    bad_channels.remove(ch)  

rawFull.drop_channels(bad_channels)
###########################
# FILTERING:

l_freq = None #1.0
h_freq = None #60.0
notch_freq = None #50.0
notch_width = None #1.0
"""
rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )
"""
###########################
# INDEPENDENT COMPONENT ANALYSIS:
n_componentsICA = None #0.999       # <---
methodICA = None #'fastica'         # <---
seed = None #99                      # <---

"""
ica = mne.preprocessing.ICA( n_components = n_componentsICA, method = methodICA, random_state=seed )
ica.fit(rawFull)  # bad segments that were marked in the EEG signal will be excluded.
#ica.plot_sources(rawFull)
ica.apply(rawFull)
"""
###########################
# RE-REFERENCING:
recordingElectrodes = ["25"]               # <---
referenceElectrodes = ["13", "15"]          # <---

rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes, verbose = True )[0]       #  <---
###########################








raws_perFreqCombCond, freqCombCond_list, trial_list = RohBlock.get_rawsPerFreqCombCond( rawFull, pathVMRK, blockDict, blockLength )
voltages_list      = list()
times_list         = list()

for rawBlock in raws_perFreqCombCond:

    voltageUnit = "V"
    voltage, times = mne.io.Raw.get_data(
            rawBlock,
            picks         = recordingElectrodes, 
            return_times  = True, 
            units         = voltageUnit,
            verbose       = True
    )
    
    voltages_list.append( voltage )
    times_list.append( times )






poss_freqCombConds = []
for freqCombCond in freqCombCond_list:
    if freqCombCond not in poss_freqCombConds:
        poss_freqCombConds.append(freqCombCond)

voltDict  = dict()
timesDict = dict()

for freqCombCond in poss_freqCombConds:
    voltDict[freqCombCond] = {
        "trial1" : None,
        "trial2" : None,
        "trial3" : None
    }
    timesDict[freqCombCond] = {
        "trial1" : None,
        "trial2" : None,
        "trial3" : None
    }





for j in range( len(raws_perFreqCombCond) ):
    voltDict[f"{freqCombCond_list[j]}"][f"{trial_list[j]}"]  = voltages_list[j]
    timesDict[f"{freqCombCond_list[j]}"][f"{trial_list[j]}"] = times_list[j] 







paramDict = {                                                 
    "file_id"             : f"participant{pNr}_mainExp{durchgang}.vhdr",                                   
 
    "recordingElectrodes" : recordingElectrodes,
    "referenceElectrodes" : referenceElectrodes,
    "badElectrodes"       : bad_channels,      

    "sfreq"               : rawFull.info["sfreq"],

    "filterParams"        : (l_freq, h_freq, notch_freq, notch_width),
    "ICAParams"           : (n_componentsICA, methodICA, seed),

    "voltageUnit"         : voltageUnit,

    "voltDict"            : voltDict,
    "timesDict"           : timesDict
}
    




pathAllResults = f"data\\results\\allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl"
AllResults.create_newAllResultsList( pathAllResults )
allResultsVolt = AllResults.loadFromPickle_allResults( pathAllResults )

allResultsVolt.append(paramDict)
AllResults.saveAsPickle_allResults( allResultsVolt, pathAllResults )

#print("Newly appended to allResults: " + COLORCYAN + f"{allResultsVolt[-1]}" + COLOREND)

    
