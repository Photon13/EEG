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

    recordingElectrodes = ["20"]               # <---
    referenceElectrodes = ["13","15"]          # <---

    identifiers = [ 
        [13, "3"],
        [4, "4"],
        [3, "3"],
        [2, "2"],
        [1, "1"],
    ]


    ##############################################################################################
    
    
    for idNr in range(len(identifiers)):

        pNr       = identifiers[idNr][0]
        durchgang = identifiers[idNr][1] 


  
        folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"

        file_id = f"participant{pNr}_mainExp{durchgang}"

        pathVHDR  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vhdr"
        pathVMRK  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vmrk"
        pathBlockDict   = f"data\\blockDict\\participant{pNr}_blockDict.txt"

        with open( pathBlockDict, "r" ) as f:
            blockDict : dict[dict] = json.load(f)


        ##############################################################################################

        typ = "threeSpeakers"

        pathAllResultsVolt      = Paths.get_pathAllResultsVolt(      pNr, durchgang, typ )
        pathAllResultsPSD       = Paths.get_pathAllResultsPSD(       pNr, durchgang, typ )
        pathAllResults_sigPeaks = Paths.get_pathAllResults_sigPeaks( pNr, durchgang, typ )
        pathAllResults_snSpeaks = Paths.get_pathAllResults_snSpeaks( pNr, durchgang, typ )

        AllResults.create_newAllResultsList( pathAllResultsVolt )
        AllResults.create_newAllResultsList( pathAllResultsPSD )
        AllResults.create_newAllResultsList( pathAllResults_sigPeaks )
        AllResults.create_newAllResultsList( pathAllResults_snSpeaks )

        allResultsVolt      = AllResults.loadFromPickle_allResults( pathAllResultsVolt )
        allResultsPSD       = AllResults.loadFromPickle_allResults( pathAllResultsPSD  )
        allResults_sigPeaks = AllResults.loadFromPickle_allResults( pathAllResults_sigPeaks )
        allResults_snSpeaks = AllResults.loadFromPickle_allResults( pathAllResults_snSpeaks )

        blocksInOrder_volt  = []
        blocksInOrder_psds  = []
        blocksInOrder_freqs = []

        ##############################################################################################


        voltDict     = {}
        psdsDict     = {}
        freqsDict    = {}
        peakDict_sig = {}
        peakDict_snS = {}

        poss_freqCombConds = BlockParams.get_possFreqCombConds()
        for freqCombCond in poss_freqCombConds:
            
            voltDict[freqCombCond]     = []
            psdsDict[freqCombCond]     = []
            freqsDict[freqCombCond]    = []
            peakDict_sig[freqCombCond] = {
                "FAM_A" : [],
                "FAM_B" : [],
                "FAM_C" : []
            }
            peakDict_snS[freqCombCond] = {
                "FAM_A" : [],
                "FAM_B" : [],
                "FAM_C" : []
            }

        ##############################################################################################



        # LADE RAW FULL:
        rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )
        ################


        # FILTERING:
        l_freq      = 1.0
        h_freq      = 60.0
        notch_freq  = 50.0
        notch_width = 1.0

        rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
        rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )
        ###########################


        # INDEPENDENT COMPONENT ANALYSIS:
        n_componentsICA = None  
        methodICA       = None    
        seed            = None             
        ###########################


        #  DROP BAD CHANNELS:
        bad_channels = []               
        for i in range(1, 64+1):
            bad_channels.append(str(i))

        used_channels = copy.deepcopy(recordingElectrodes)
        if( referenceElectrodes != None ):
            used_channels.extend(referenceElectrodes)
        for ch in used_channels :      # <---    
            bad_channels.remove(ch)  

        rawFull.drop_channels(bad_channels)
        ###########################


        # RE-REFERENCING:
        if( referenceElectrodes != None ):
            rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]
        ###########################

        # GET Z-BUSSE:
        zBusses = Ereignisse.get_zBusse( pathVMRK )
        ###########################



        # GET RAW_BLOCK RESP.:
        for blockNr in range(72):

            start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
            end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
            rawBlock  : object  = rawFull.copy().crop(tmin = start, tmax = end)

            freqComb  : str     = blockDict[f"block{blockNr}"]["freqComb"]
            condition : str     = blockDict[f"block{blockNr}"]["condition"]

            freqCombCond : str = f"{freqComb}_{condition}"

            voltage, times = mne.io.Raw.get_data(
                rawBlock,
                picks         = recordingElectrodes, 
                return_times  = True, 
                units         = "V",
            )
            voltage = voltage[0]

            len_interval = 5000  # 10 sec
            start = 1            # FIRSTMOST SAMPLE REMOVED (BECAUSE RAWBLOCK IS 15001 SAMPLES LONG)
            end   = start + len_interval

            while( end <= 15001 ): #len rawBlock
                voltage_subArray = copy.deepcopy( voltage[start:end])
                voltDict[freqCombCond].append(voltage_subArray)
                start = start + int(len_interval/2) #verschiebe start (50% Überlapp)
                end   = start + len_interval   

                ##
                blocksInOrder_volt.append(voltage_subArray) 
                ##
                  
            # ALLE SUBARRAYS 5000 SAMPLES (=10 SEC) LANG
            # PER RAWBLOCK 5 INTERVALLE VON JE 10 SECS



        ##########################################################################################

        

        for freqCombCond in voltDict:
            for intervalNr in range( len(voltDict[freqCombCond]) ):
                voltage = voltDict[freqCombCond][intervalNr]

                freqs, psds = scipy.signal.periodogram(
                    x       = voltage,
                    fs      = rawFull.info["sfreq"],
                    scaling = "density" 
                )

                psdsDict[freqCombCond].append(  psds  )
                freqsDict[freqCombCond].append( freqs )

        ##
        for voltage in blocksInOrder_volt:
            freqs, psds = scipy.signal.periodogram(
                x       = voltage,
                fs      = rawFull.info["sfreq"],
                scaling = "density" 
            )
            blocksInOrder_psds.append(psds)
            blocksInOrder_freqs.append(freqs)
        ##


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

                    if( 0.05 >= p_value ):
                        peakDict_sig[freqCombCond][famName].append(psd_peak)
                    peakDict_snS[freqCombCond][famName].append(psd_peak)



        ##########################################################################################



        info = {                                                 
            "file_id"             : f"participant{pNr}_mainExp{durchgang}.vhdr",                                   
        
            "recordingElectrodes" : recordingElectrodes,
            "referenceElectrodes" : referenceElectrodes,     

            "sfreq"               : rawFull.info["sfreq"],

            "filterParams"        : (l_freq, h_freq, notch_freq, notch_width),
            "ICAParams"           : (n_componentsICA, methodICA, seed),
        }


        newEntry_allResultsVolt      = copy.deepcopy( info )
        newEntry_allResultPSD        = copy.deepcopy( info )
        newEntry_allResults_sigPeaks = copy.deepcopy( info )
        newEntry_allResults_snSpeaks = copy.deepcopy( info )



        newEntry_allResultsVolt["voltDict"]          = voltDict
        newEntry_allResultPSD["psdsDict"]            = psdsDict
        newEntry_allResultPSD["freqsDict"]           = freqsDict
        newEntry_allResults_sigPeaks["peakDict_sig"] = peakDict_sig
        newEntry_allResults_snSpeaks["peakDict_snS"] = peakDict_snS

        ##
        newEntry_allResultsVolt["blocksInOrder_volt"] = blocksInOrder_volt
        newEntry_allResultPSD["blocksInOrder_psds"]   = blocksInOrder_psds
        newEntry_allResultPSD["blocksInOrder_freqs"]  = blocksInOrder_freqs
        ##


        allResultsVolt.append(      newEntry_allResultsVolt      )
        allResultsPSD.append(       newEntry_allResultPSD        )
        allResults_sigPeaks.append( newEntry_allResults_sigPeaks )
        allResults_snSpeaks.append( newEntry_allResults_snSpeaks )

        AllResults.saveAsPickle_allResults( allResultsVolt,      pathAllResultsVolt      )
        AllResults.saveAsPickle_allResults( allResultsPSD,       pathAllResultsPSD       )
        AllResults.saveAsPickle_allResults( allResults_sigPeaks, pathAllResults_sigPeaks )
        AllResults.saveAsPickle_allResults( allResults_snSpeaks, pathAllResults_snSpeaks )

        ##########################################################################################



getallResults()