import mne
import json
import copy
import numpy as np
import scipy
from scipy import stats
from typing import List

from Paths import Paths
from BlockParams import BlockParams
from Ereignisse import Ereignisse
from AllResults import AllResults
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




def getallResults():

    recordingElectrodes = ["14"]               # <---
    referenceElectrodes = ["13","15"]          # <---

    identifiers = [                     # <---
        [13, "3"],
        #[4, "4"],
        #[3, "3"],
        #[2, "2"],
        #[1, "1"],
    ]

    expType = "threeSpeakers"           # <---
    #expType = "singleSpeaker"

    ##############################################################################################
    
    if( expType == "threeSpeakers" ):
        poss_freqCombConds = BlockParams.get_possFreqCombConds()
        keyNames = poss_freqCombConds
    elif( expType == "singleSpeaker" ):
        attentionArten = ["max_attention", "min_attention"]
        keyNames = attentionArten

    ##############################################################################################
    
    for idNr in range(len(identifiers)):

        pNr       = identifiers[idNr][0]
        durchgang = identifiers[idNr][1] 


        folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"

        if( expType == "threeSpeakers" ):
            file_id = f"participant{pNr}_mainExp{durchgang}"
        elif( expType == "singleSpeaker" ):
            file_id = f"participant{pNr}_singleSpeaker"

        pathVHDR  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vhdr"
        pathVMRK  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vmrk"
        pathBlockDict   = f"data\\blockDict\\participant{pNr}_blockDict.txt"

        with open( pathBlockDict, "r" ) as f:
            blockDict : dict[dict] = json.load(f)

        ##############################################################################################
        # INIT DICTS:
        #
        voltDict      = {}
        psdsDict      = {}
        freqsDict     = {}
        peaksSig_quot = {}
        peaksSnS_quot = {}

        for keyName in keyNames:
            voltDict[keyName]      = []
            psdsDict[keyName]      = []
            freqsDict[keyName]     = []
            peaksSig_quot[keyName] = {
                "FAM_A" : [],
                "FAM_B" : [],
                "FAM_C" : []
            }
            peaksSnS_quot[keyName] = {
                "FAM_A" : [],
                "FAM_B" : [],
                "FAM_C" : []
            }
        ##############################################################################################
        # INIT LISTS:

        voltInOrder  = []
        psdsInOrder  = []
        freqsInOrder = []
        peaksInOrder = {
            "FAM_A" : [],
            "FAM_B" : [],
            "FAM_C" : []
        }
        ##############################################################################################
        # RAW PRE_PROCESSING:
        #
        rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )

        l_freq      = 1.0
        h_freq      = 60.0
        notch_freq  = 50.0
        notch_width = 1.0

        rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
        rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )

        n_componentsICA = None  
        methodICA       = None    
        seed            = None
        
        bad_channels = []               
        for i in range(1, 64+1):
            bad_channels.append(str(i))

        used_channels = copy.deepcopy(recordingElectrodes)
        if( referenceElectrodes != None ):
            used_channels.extend(referenceElectrodes)
        for ch in used_channels :      # <---    
            bad_channels.remove(ch)  

        rawFull.drop_channels(bad_channels)

        rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]

        ##############################################################################################
        # GET VOLTAGE PER INTERVAL :
        #
        zBusses = Ereignisse.get_zBusse( pathVMRK )
        n_blocks = len(zBusses)

        if( expType == "threeSpeakers" ):
            blockLength = BlockParams.DEFAULT_BLOCK_LENGTH
            keyNames = BlockParams.get_possFreqCombConds()
        elif( expType == "singleSpeaker" ):
            blockLength = int(60*2.5) #2.5 min

        ##
        for i in range(n_blocks):

            if( expType == "threeSpeakers" ):
                freqComb     : str   = blockDict[f"block{i}"]["freqComb"]
                condition    : str   = blockDict[f"block{i}"]["condition"]
                freqCombCond : str   = f"{freqComb}_{condition}"
                keyName      :str    = freqCombCond

            elif( expType == "singleSpeaker" ):
                attentionArt : str = attentionArten[i]
                keyName      : str = attentionArt


            start     : float   = float( zBusses[ i ] ) / float( rawFull.info["sfreq"] ) #sec
            end       : float   = float( start + blockLength )                           #sec
            rawBlock  : object  = rawFull.copy().crop(tmin = start, tmax = end)

            voltage, times = mne.io.Raw.get_data(
                rawBlock,
                picks         = recordingElectrodes, 
                return_times  = True, 
                units         = "V",
            )
            voltage = voltage[0]

            len_rawBlock = (blockLength*500)+1
            start : int  = 1                    # FIRSTMOST SAMPLE REMOVED
            end   : int  = start + 5000         # 10 sec
            while( end <= (len_rawBlock) ):
                voltage_subArray = copy.deepcopy( voltage[start:end] )
                voltDict[keyName].append( voltage_subArray )
                start = start + 2500            #verschiebe start um 5 sec (müsste 50% Überlapp entsprechen)
                end   = start + 5000            #10 sec       
                # ALLE INTERVALLE 5000 SAMPLES (=10 SEC) LANG
                voltInOrder.append( voltage_subArray)

        ##############################################################################################
        ##############################################################################################
        # GET PSD PER INTERVAL:
        #
        for keyName in voltDict:
            for intervalNr in range( len(voltDict[keyName]) ):
                voltage = voltDict[keyName][intervalNr]

                freqs, psds = scipy.signal.periodogram(
                    x       = voltage,
                    fs      = rawFull.info["sfreq"],
                    scaling = "density" 
                )

                psdsDict[keyName].append(  psds  )
                freqsDict[keyName].append( freqs )


        # GET PSDS_IN_ORDER:
        #
        for voltage in voltInOrder:
            freqs, psds = scipy.signal.periodogram(
                    x       = voltage,
                    fs      = rawFull.info["sfreq"],
                    scaling = "density" 
            )
            psdsInOrder.append( psds )
            freqsInOrder.append( freqs )

        ##############################################################################################
        ##############################################################################################
        # GET PEAKS (NORMALISED):
        #
        for freqCombCond in psdsDict:
            for intervalNr in range( len(psdsDict[freqCombCond]) ):

                psds  = psdsDict[freqCombCond][intervalNr]
                freqs = freqsDict[freqCombCond][intervalNr]

                for famName in BlockParams.FAMS_ABC:
                    fam                = BlockParams.FAMS_ABC[famName]
                    i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                    psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                    psd_peak           = psds[i_largestVal]
                    statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                    meanPsd_noise = np.mean(psds_neighbours)
                    quot = psd_peak / float(meanPsd_noise)
                    if( 0.05 >= p_value ):
                        peaksSig_quot[freqCombCond][famName].append(quot)
                    peaksSnS_quot[freqCombCond][famName].append(quot)

        # GET PEAKS (NORMALISED) IN ORDER:
        #
        for k in range( len(psdsInOrder) ):
            psds  = psdsInOrder[k]
            freqs = freqsInOrder[k]

            for famName in BlockParams.FAMS_ABC:
                fam                = BlockParams.FAMS_ABC[famName]
                i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                psd_peak           = psds[i_largestVal]
                # include all peaks, not only sig ones
                meanPsd_noise = np.mean(psds_neighbours) 
                quot = psd_peak / float(meanPsd_noise)
                peaksInOrder[famName].append(quot)

        ##############################################################################################
        ##############################################################################################
        # SAVE ALL_RESULTS:
        #
        pathAllResults = Paths.get_pathAllResults( pNr, durchgang, expType )
        AllResults.create_newAllResultsList( pathAllResults )
        allResults : List[dict] = AllResults.loadFromPickle_allResults( pathAllResults )

        info = {                                                 
            "file_id"             : file_id,

            "epoching"            : True,                                   
        
            "recordingElectrodes" : recordingElectrodes,
            "referenceElectrodes" : referenceElectrodes,     

            "sfreq"               : rawFull.info["sfreq"],

            "filterParams"        : (l_freq, h_freq, notch_freq, notch_width),
            "ICAParams"           : (n_componentsICA, methodICA, seed),

            "voltDict"            : voltDict,
            "psdsDict"            : psdsDict,
            "freqsDict"           : freqsDict,
            "peaksSig_quot"       : peaksSig_quot,
            "peaksSnS_quot"       : peaksSnS_quot,

            "voltInOrder"         : voltInOrder,
            "psdsInOrder"         : psdsInOrder,
            "freqsInOrder"        : freqsInOrder,
            "peaksInOrder"        : peaksInOrder
        }
        allResults.append(info)
        AllResults.saveAsPickle_allResults( allResults, pathAllResults )

getallResults()

