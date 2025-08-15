import mne
import json
import copy
import numpy as np
from typing import List

from BlockParams import BlockParams
from Ereignisse import Ereignisse
from AllResults import AllResults

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'





# CHOOSE PARTICIPANT:
pNr = 2                     # <---            
durchgang = "2"             # <---      
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
################


# ASSIGN BAD BLOCKS:
bad_blockNrs : List[int] = []       # <---
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
filtering : bool = False        # <--- 

if( filtering == True ):
    l_freq = 1.0
    h_freq = 60.0
    notch_freq = 50.0
    notch_width = 1.0
else:
    l_freq = None
    h_freq = None
    notch_freq = None
    notch_width = None

if( notch_freq != None and notch_width != None ):
    print( COLORRED + "NOTCH FILTER ACTIVE." + COLOREND )
    rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
if( l_freq != None and h_freq != None ):
    print( COLORRED + "HIGH-PASS AND LOW-PASS FILTER ACTIVE." + COLOREND )
    rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )
###########################


# INDEPENDENT COMPONENT ANALYSIS:
applyICA = False                        # <---

if( applyICA == True ):
    n_componentsICA = 0.999   
    methodICA       = 'fastica'      
    seed            = 99   
else:
    n_componentsICA = None  
    methodICA       = None     
    seed            = None              

if( n_componentsICA != None and methodICA != None and seed != None ):
    print( COLORRED + "ICA APPLIED." + COLOREND )
    ica = mne.preprocessing.ICA( n_components = n_componentsICA, method = methodICA, random_state=seed )
    ica.fit(rawFull)  # bad segments that were marked in the EEG signal will be excluded.
    #ica.plot_sources(rawFull)
    ica.apply(rawFull)

###########################


# RE-REFERENCING:
recordingElectrodes = ["25"]               # <---
referenceElectrodes = ["13", "15"]          # <---

rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]       #  <---
###########################


zBusses = Ereignisse.get_zBusse( pathVMRK )
rawDict = copy.deepcopy(BlockParams.get_musterDict())

""" 
RAW_DICT:

    rawDict[<freqCombCond>]["trial0"] # contains list (and later concatenated raw) of rawBlock for each trial
    rawDict[<freqCombCond>][trial1]   # contains raw for trial 1
    ...
    rawDict[<freqCombCond>][trial3]   # contains raw for trial 3
"""

# GET RAW_BLOCK RESP.:
for blockNr in range(72):
    if( blockNr not in bad_blockNrs ):

        start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
        end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
        rawBlock  : object = rawFull.copy().crop(tmin = start, tmax = end)

        freqComb  : str     = blockDict[f"block{blockNr}"]["freqComb"]
        condition : str     = blockDict[f"block{blockNr}"]["condition"]
        trialNr   : str     = blockDict[f"block{blockNr}"]["trial"]

        freqCombCond : str = f"{freqComb}_{condition}"
        rawDict[freqCombCond][f"trial{trialNr}"] = rawBlock

        if( rawDict[freqCombCond][f"trial0"] == None ):
            rawDict[freqCombCond][f"trial0"] = [] #init new list
        
        rawDict[freqCombCond][f"trial0"].append( copy.deepcopy(rawBlock)) #append trial to dict[...]["trial0"]



# CONCATENATE TRIALS and INSERT RAW_CONCAT INTO RAW_DICT["FREQ_COMB_COND"]["TRIAL0"]
for freqCombCond in rawDict:
    mne.concatenate_raws( rawDict[freqCombCond][f"trial0"] ) #modifies 1st raw in list in-place
    rawDict[freqCombCond][f"trial0"] = rawDict[freqCombCond][f"trial0"][0]
    
    indices_badAnnotations = np.where( rawDict[freqCombCond][f"trial0"].annotations.description == "BAD boundary")
    rawDict[freqCombCond][f"trial0"].annotations.delete( indices_badAnnotations ) #works





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




list_allGoodRaws = []
for freqCombCond in rawDict: #at this point
    for trial in rawDict[freqCombCond]:
        if( trial != "trial0" and rawDict[freqCombCond][trial] != None ):
            list_allGoodRaws.append( rawDict[freqCombCond][trial] )

mne.concatenate_raws( list_allGoodRaws )
rawConcat_allGoodRaws = list_allGoodRaws[0]

indices_badAnnotations = np.where( rawConcat_allGoodRaws.annotations.description == "BAD boundary")
rawConcat_allGoodRaws.annotations.delete( indices_badAnnotations )

voltage_concatAllGoodBlocks, times_concatAllGoodBlocks = mne.io.Raw.get_data(
    rawConcat_allGoodRaws,
    picks         = recordingElectrodes, 
    return_times  = True, 
    units         = "V",
)
print( f"huhu {times_concatAllGoodBlocks}")

paramDict = {                                                 
    "file_id"             : f"participant{pNr}_mainExp{durchgang}.vhdr",                                   
 
    "recordingElectrodes" : recordingElectrodes,
    "referenceElectrodes" : referenceElectrodes,
    "badElectrodes"       : bad_channels,      

    "sfreq"               : rawFull.info["sfreq"],

    "filterParams"        : (l_freq, h_freq, notch_freq, notch_width),
    "ICAParams"           : (n_componentsICA, methodICA, seed),

    "voltDict"                    : voltDict,
    "voltage_concatAllGoodBlocks" : voltage_concatAllGoodBlocks
}


pathAllResults = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\allResults\\allResultsVolt_participant{pNr}_mainExp{durchgang}.pkl"
AllResults.create_newAllResultsList( pathAllResults )
allResultsVolt = AllResults.loadFromPickle_allResults( pathAllResults )

allResultsVolt.append(paramDict)
AllResults.saveAsPickle_allResults( allResultsVolt, pathAllResults )
#dict append bad block nrs