import pandas as pd
import numpy as np
from typing import List
import pickle

from IPython import display

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


class AllResults:
    """ allResults ist eine Liste von Dictionaries
        Jeder Listen-Eintrag entspricht dem Ergebnis der Voltage- und Psd-Berechnung für eine condFreqComb mit angegebenen Parametern
    """

    @staticmethod
    def appendResult_toAllResults( 
        allResults          : List[dict],                               
        file_id             : str,                                     
        freqCombCond        : str,
        recordingElectrodes : List[str],
        referenceElectrodes : List[str]                  | None, 
        filterParams        : tuple[str | int | None],
        ICAParams           : tuple[float]               | None, 
        fourierParams       : tuple[float], 
        voltageTimes        : tuple[np.ndarray | None], 
        psdsFreqs           : tuple[np.ndarray | None] 
    ):
        """     file_id             : \"participant<>_mainExp<>.vhdr\",
                freqCombCond        : \"\<fams LMR\>_\<target\>\" #z.B. ABC_left,
                recordingElectrodes : [ \'\<\>' , '\<\>' ],
                referenceElectrodes : [ \'\<\>\' , \'\<\>\' ], 
                filterParams        : (l_freq, h_freq, notch_freq, notch_width),
                ICAParams           : \<str\>,  #?                                    
                fourierParams       : (nfft, n_per_seg, n_overlap), 
                voltage_times       : (voltage, times), 
                psds_freqs          : (psds, psds_dB, freqs)

                # order of recordingElectrodes is perserved inside of 
                # voltage, times, psds, psds_dB and freqs
        """
        
        newDict = {
            "file_id"             : file_id,
            "freqCombCond"        : freqCombCond,
            "recordingElectrodes" : recordingElectrodes,
            "referenceElectrodes" : referenceElectrodes, 
            "filterParams"        : filterParams,
            "ICAParams"           : ICAParams,
            "fourierParams"       : fourierParams, 
            "voltage_times"       : voltageTimes, 
            "psds_freqs"          : psdsFreqs 
        }
        allResults.append(newDict)
        return allResults


    @staticmethod
    def saveAsPickle_allResults( allResults : List[dict], path : str ):
        with open(path, "wb") as f:
            pickle.dump(allResults, f)


    @staticmethod
    def loadFromPickle_allResults( path : str ) -> pd.DataFrame:
        with open(path, "rb") as f:
            allResults = pickle.load(f)
        return allResults



