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



identifiers = [ 
    [13, "3"],
    [4, "4"],
    [3, "3"],
    [2, "2"],
    [1, "1"],
]


for idNr in range(len(identifiers)):
    pNr = identifiers[idNr][0]
    durchgang = identifiers[idNr][1] 


    # SET PATHS:
    folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"

    pathVHDR : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vhdr"
    pathVMRK : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vmrk"
    pathBlockDict = f"data\\blockDict\\participant{pNr}_blockDict.txt"

    with open( pathBlockDict, "r" ) as f:
        blockDict : dict[dict] = json.load(f)
    ###########################


    # LADE RAW FULL:
    rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )
    ################


    # FILTERING:
    filtering : bool = True        # <--- 

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


    #  DROP BAD CHANNELS:
    bad_channels = []               
    for i in range(1, 64+1):
        bad_channels.append(str(i))

    for ch in ["8", "13", "15"] :      # <---    
        bad_channels.remove(ch)  

    rawFull.drop_channels(bad_channels)
    ###########################


    # RE-REFERENCING:
    recordingElectrodes = ["8"]               # <---
    referenceElectrodes = ["13", "15"]          # <---

    rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]
    ###########################




    zBusses = Ereignisse.get_zBusse( pathVMRK )
    voltDict = {}
    poss_freqCombConds = BlockParams.get_possFreqCombConds()
    for freqCombCond in poss_freqCombConds:
        voltDict[freqCombCond] = []




    # GET RAW_BLOCK RESP.:
    for blockNr in range(72):

            start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
            end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
            rawBlock  : object = rawFull.copy().crop(tmin = start, tmax = end)

            freqComb  : str     = blockDict[f"block{blockNr}"]["freqComb"]
            condition : str     = blockDict[f"block{blockNr}"]["condition"]
            trialNr   : str     = blockDict[f"block{blockNr}"]["trial"]

            freqCombCond : str = f"{freqComb}_{condition}"

            voltage, times = mne.io.Raw.get_data(
                rawBlock,
                picks         = recordingElectrodes, 
                return_times  = True, 
                units         = "V",
            )
            voltage = voltage[0]

            voltage_subArray1 = copy.deepcopy( voltage[1:5001])
            voltage_subArray2 = copy.deepcopy( voltage[5001:10001])
            voltage_subArray3 = copy.deepcopy( voltage[10001:15001])
            # ALL SUBARRAYS 5000 SAMPLES (=10 SEC) LONG
            # FIRSTMOST SAMPLE REMOVED (BECAUSE RAWBLOCK IS 15001 SAMPLES LONG)

            voltDict[freqCombCond].append(voltage_subArray1)
            voltDict[freqCombCond].append(voltage_subArray2)
            voltDict[freqCombCond].append(voltage_subArray3)




    newEntry_allResultsEpochsVolt = {                                                 
        "file_id"             : f"participant{pNr}_mainExp{durchgang}.vhdr",                                   
    
        "recordingElectrodes" : recordingElectrodes,
        "referenceElectrodes" : referenceElectrodes,
        "badElectrodes"       : bad_channels,      

        "sfreq"               : rawFull.info["sfreq"],

        "filterParams"        : (l_freq, h_freq, notch_freq, notch_width),
        "ICAParams"           : (n_componentsICA, methodICA, seed),

        "voltDict"            : voltDict
    }


    pathAllResults = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results Epochs\\allResultsEpochs\\allResultsEpochsVolt_participant{pNr}_mainExp{durchgang}.pkl"
    AllResults.create_newAllResultsList( pathAllResults )
    allResultsEpochsVolt = AllResults.loadFromPickle_allResults( pathAllResults )

    allResultsEpochsVolt.append(newEntry_allResultsEpochsVolt)
    AllResults.saveAsPickle_allResults( allResultsEpochsVolt, pathAllResults )