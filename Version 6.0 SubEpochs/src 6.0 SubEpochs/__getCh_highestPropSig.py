from itertools import combinations
import mne 
import scipy
from scipy import stats
import copy
import numpy as np
import os

from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from Ereignisse import Ereignisse
from BlockParams import BlockParams
from Plots import Plots


COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'



# BENÖTIGT CA. 1.5-2 h fÜR 32 ELEKTRODEN
def get_voltageList(rawFull_reRef, zBusses, recordingElectrode):
    voltageList = []
    ####
    for blockNr in range(72):
        start     : float   = float( zBusses[ blockNr ] ) / float( rawFull_reRef.info["sfreq"] )
        end       : float   = float( start + BlockParams.DEFAULT_BLOCK_LENGTH )
        rawBlock  : object  = rawFull_reRef.copy().crop(tmin = start, tmax = end)

        voltage, times = mne.io.Raw.get_data(
            rawBlock,
            picks         = [recordingElectrode], 
            return_times  = True, 
            units         = "V",
        )
        voltage = voltage[0]

        start = 1            # FIRSTMOST SAMPLE REMOVED (BECAUSE RAWBLOCK IS 15001 SAMPLES LONG)
        end   = start + 5000 # 10 sec

        while( end <= 15001 ): #len rawBlock
            voltage_subArray = copy.deepcopy( voltage[start:end])
            voltageList.append(voltage_subArray)
            start = start + 2500  #verschiebe start um 5 sec (müsste 50% Überlapp entsprechen)
            end   = start + 5000  #10 sec 

    return voltageList



def get_psdsAndFreqsList(voltageList, sfreq):
    psdsList  = []
    freqsList = []
    ####
    for voltage in voltageList:
        freqs, psds = scipy.signal.periodogram(
            x       = voltage,
            fs      = sfreq,
            scaling = "density" 
        )
        psdsList.append(psds)
        freqsList.append(freqs)
    return psdsList, freqsList



def get_sigPropDict(rawFull, zBusses):
    sigPropDict = {}

    channels = rawFull.info["ch_names"]
    #print(COLORRED + f"{channels}" + COLOREND)
    chCombos = list( combinations( channels, 2) )
    #print(COLORGREEN + f"{chCombos}" + COLOREND)
    #for chCombo in chCombos:
    #for chCombo in [('1', '9'),('1', '10'),('1', '11')]:
    for k in range( len(chCombos) ):
        chCombo = list(chCombos[k])
        print(chCombo)
        recordingElectrode = (chCombo[0])
        referenceElectrode = (chCombo[1])
        #print(referenceElectrode)
        rawFull_reRef = copy.deepcopy( rawFull )
        rawFull_reRef = mne.set_eeg_reference( rawFull_reRef, ref_channels = [referenceElectrode] )[0]
   
        voltageList = get_voltageList(rawFull_reRef, zBusses, recordingElectrode)
        psdsList, freqsList = get_psdsAndFreqsList(voltageList, rawFull_reRef.info["sfreq"])      


        sigPropDict[f"{recordingElectrode}_{referenceElectrode}"] = {
            "n_sig"    : 0,
            "n_nonSig" : 0
        }

        for j in range( len( psdsList) ): #loop through blockIntervals
            psds  = psdsList[j]
            freqs = freqsList[j]

            for famName in BlockParams.FAMS_ABC:
                fam                = BlockParams.FAMS_ABC[famName]
                i_largestVal       = HelpClass_PeakAnalysis.get_indexLargestValue_nextFam( fam, psds, freqs )
                psds_neighbours    = HelpClass_PeakAnalysis.get_PSDneighbours( fam, psds, freqs )
                psd_peak           = psds[i_largestVal]
                statistic, p_value = stats.f_oneway( psd_peak, psds_neighbours )

                if( 0.05 >= round(p_value, 1) ): #3
                    sigPropDict[f"{recordingElectrode}_{referenceElectrode}"]["n_sig"] += 1
                    print("huhu")
                else:
                    sigPropDict[f"{recordingElectrode}_{referenceElectrode}"]["n_nonSig"] += 1
    
    return sigPropDict




def getCh_highestPropSig():

    identifiers = [    # <---
        #[13, "3"],
        #[4, "4"],
        #[3, "3"],
        [2, "2"],
        #[1, "1"],
    ]

    ####
    for idNr in range(len(identifiers)):

        pNr       = identifiers[idNr][0]
        durchgang = identifiers[idNr][1] 

        folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"
        file_id = f"participant{pNr}_mainExp{durchgang}"
        pathVHDR  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vhdr"
        pathVMRK  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vmrk"

        rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )

        bad_channels = []               
        for i in range(33, 64+1):
            bad_channels.append(str(i))
        rawFull.drop_channels(bad_channels) #drop yellow electrodes


        zBusses = Ereignisse.get_zBusse( pathVMRK )

        sigPropDict = get_sigPropDict(rawFull, zBusses)

        ####

        highestProp = 0.0
        chComb_highestProp = "None"
        for chComb in sigPropDict:
            n_sig    = sigPropDict[chComb]["n_sig"]
            n_nonSig = sigPropDict[chComb]["n_nonSig"]
            prop     = float(n_sig) / float(n_sig + n_nonSig)
            if( prop > highestProp ):
                highestProp        = prop
                chComb_highestProp = f"{chComb}"

        print(f"{chComb_highestProp} {highestProp}")


getCh_highestPropSig()

#participant2 best: 20 Vs 13: propSig=0.26 (für Rundung 1 Stelle Nachkomma)