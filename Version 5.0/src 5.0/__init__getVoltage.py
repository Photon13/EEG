import mne
import json
import copy
import numpy as np
from typing import List

from BlockParams import BlockParams
from Ereignisse import Ereignisse

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'





# CHOOSE PARTICIPANT:
pNr = 4                     # <---            
durchgang = "4"             # <---      
###########################


# SET PATHS:
folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"

pathVHDR : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vhdr"
pathVMRK : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vmrk"
pathBlockDict = f"data\\blockDict\\participant{pNr}_blockDict.txt"

with open( pathBlockDict, "r" ) as f:
    blockDict : dict[dict] = json.load(f)
###########################


# LADE RAW FULL:
rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )

#rawFull.plot()        # <---
################


# ASSIGN BAD BLOCKS:
bad_blockNrs : List[int] = []  # <---
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


zBusses = Ereignisse.get_zBusse( pathVMRK )
rawDict = copy.deepcopy(BlockParams.get_musterDict())

for blockNr in range(72):
    if( blockNr not in bad_blockNrs ):

        start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
        end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
        rawBlock  : object = rawFull.copy().crop(tmin = start, tmax = end)

        freqComb  : str     = blockDict[f"block{blockNr}"]["freqComb"]
        condition : str     = blockDict[f"block{blockNr}"]["condition"]
        trialNr   : str   = blockDict[f"block{blockNr}"]["trial"]

        freqCombCond : str = f"{freqComb}_{condition}"
        rawDict[freqCombCond][f"trial{trialNr}"] = rawBlock

        if( rawDict[freqCombCond][f"trial0"] == None ):
            rawDict[freqCombCond][f"trial0"] = [] #init new list
        
        rawDict[freqCombCond][f"trial0"].append( copy.deepcopy(rawBlock))


for freqCombCond in rawDict:
    mne.concatenate_raws( rawDict[freqCombCond][f"trial0"] ) #modifies 1st raw in list in-place

    indices_badAnnotations = np.where( rawDict[freqCombCond][f"trial0"][0].annotations.description == "BAD boundary")
    rawDict[freqCombCond][f"trial0"][0].annotations.delete( indices_badAnnotations ) #works

    rawDict[freqCombCond][f"trial0"] = rawDict[freqCombCond][f"trial0"][0]


print(rawDict)


voltDict  = copy.deepcopy(BlockParams.get_musterDict())
timesDict = copy.deepcopy(BlockParams.get_musterDict())

for freqCombCond in rawDict:
    for trial in rawDict[freqCombCond]:

        raw_trial = rawDict[freqCombCond][trial]
        voltage, times = mne.io.Raw.get_data(
                raw_trial,
                picks         = recordingElectrodes, 
                return_times  = True, 
                units         = "V",
        )
        voltDict[freqCombCond][trial]  = voltage[0]
        timesDict[freqCombCond][trial] = times[0]



print(voltDict)
print(timesDict)

#dict append bad block nrs