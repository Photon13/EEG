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
    referenceElectrodes = ["13", "15"]          # <---

    identifiers = [ 
        [13, "3"],
        [4, "4"],
        [3, "3"],
        [2, "2"],
        [1, "1"],
    ]


    ##############################################################################################
    
    
    for idNr in range(len(identifiers)):

        pNr = identifiers[idNr][0]
        durchgang = identifiers[idNr][1] 


  
        folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"

        pathVHDR : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vhdr"
        pathVMRK : str = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp{durchgang}.vmrk"
        pathBlockDict = f"data\\blockDict\\participant{pNr}_blockDict.txt"

        with open( pathBlockDict, "r" ) as f:
            blockDict : dict[dict] = json.load(f)


        ##############################################################################################


        pathAllResultsSubEpochsVolt = Paths.get_pathAllResultsSubEpochsVolt(pNr, durchgang)
        pathAllResultsSubEpochsPSD  = Paths.get_pathAllResultsSubEpochsPSD(pNr, durchgang)
        pathAllResults_sigPeaks     = Paths.get_pathAllResults_sigPeaks(pNr, durchgang)
        pathAllResults_snSpeaks     = Paths.get_pathAllResults_snSpeaks(pNr, durchgang)

        AllResults.create_newAllResultsList( pathAllResultsSubEpochsVolt )
        AllResults.create_newAllResultsList( pathAllResultsSubEpochsPSD )
        AllResults.create_newAllResultsList( pathAllResults_sigPeaks )
        AllResults.create_newAllResultsList( pathAllResults_snSpeaks )

        allResultsSubEpochsVolt = AllResults.loadFromPickle_allResults( pathAllResultsSubEpochsVolt )
        allResultsSubEpochsPSD  = AllResults.loadFromPickle_allResults( pathAllResultsSubEpochsPSD  )
        allResults_sigPeaks     = AllResults.loadFromPickle_allResults( pathAllResults_sigPeaks )
        allResults_snSpeaks     = AllResults.loadFromPickle_allResults( pathAllResults_snSpeaks )


        ##############################################################################################


        voltDict   =  {}
        psdsDict   = {}
        freqsDict  = {}
        peakDict_sig = {}
        peakDict_snS = {}

        poss_freqCombConds = BlockParams.get_possFreqCombConds()
        for freqCombCond in poss_freqCombConds:
            
            voltDict[freqCombCond] = []
            psdsDict[freqCombCond] = []
            freqsDict[freqCombCond] = []
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
        l_freq = 1.0
        h_freq = 60.0
        notch_freq = 50.0
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

        used_channels = copy.deepcopy(recordingElectrodes).extend(referenceElectrodes)
        for ch in used_channels :      # <---    
            bad_channels.remove(ch)  

        rawFull.drop_channels(bad_channels)
        ###########################


        # RE-REFERENCING:
        rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]
        ###########################

        # GET Z-BUSSE:
        zBusses = Ereignisse.get_zBusse( pathVMRK )
        ###########################



        # GET RAW_BLOCK RESP.:
        for blockNr in range(72):

            start     : float   = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
            end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
            rawBlock  : object = rawFull.copy().crop(tmin = start, tmax = end)

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



            start = 1 # FIRSTMOST SAMPLE REMOVED (BECAUSE RAWBLOCK IS 15001 SAMPLES LONG)
            end = start + 5000 # 10 sec

            while( end <= 15001 ): #len rawBlock
                voltage_subArray = copy.deepcopy( voltage[start:end])
                voltDict[freqCombCond].append(voltage_subArray)
                start = start + 2500 #verschiebe start um 5 sec (müsste 50% Überlapp entsprechen)
                end = start + 5000  #10 sec       
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

                psdsDict[freqCombCond].append( psds )
                freqsDict[freqCombCond].append( freqs )

        


        for freqCombCond in psdsDict[freqCombCond]:
            for intervalNr in range( len(psdsDict[freqCombCond]) ):

                psds  = psdsDict[freqCombCond][intervalNr]
                freqs = freqsDict[freqCombCond][intervalNr]

                for famName in BlockParams.FAMS_ABC:
                    fam = BlockParams.FAMS_ABC[famName]
                    i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                    psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                    psd_peak           = psds[i_largestVal]
                    statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                    if( 0.05 >= round(p_value, 1) ):
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
        newEntry_allResultsEpochsPSD = copy.deepcopy( info )
        newEntry_allResults_sigPeaks = copy.deepcopy( info )
        newEntry_allResults_snSpeaks = copy.deepcopy( info )



        newEntry_allResultsVolt["voltDict"] = voltDict
        newEntry_allResultsEpochsPSD["psdsDict"]  = psdsDict
        newEntry_allResultsEpochsPSD["freqsDict"] = freqsDict
        newEntry_allResults_sigPeaks["peakDict_sig"] = peakDict_sig
        newEntry_allResults_snSpeaks["peakDict_snS"] = peakDict_snS



        allResultsSubEpochsVolt.append( newEntry_allResultsVolt )
        allResultsSubEpochsPSD.append( newEntry_allResultsEpochsPSD )
        allResults_sigPeaks.append( newEntry_allResults_sigPeaks )
        allResults_snSpeaks.append( newEntry_allResults_snSpeaks )

        AllResults.saveAsPickle_allResults( allResultsSubEpochsVolt, pathAllResultsSubEpochsVolt )
        AllResults.saveAsPickle_allResults( allResultsSubEpochsPSD, pathAllResultsSubEpochsPSD )
        AllResults.saveAsPickle_allResults( allResults_sigPeaks, pathAllResults_sigPeaks )
        AllResults.saveAsPickle_allResults( allResults_snSpeaks, pathAllResults_snSpeaks )

        ##########################################################################################



getallResults()