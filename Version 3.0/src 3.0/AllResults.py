import pandas as pd
import numpy as np
from typing import List
import pickle
import os.path
import sys

from IPython import display

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'

class AllResults:

    @staticmethod
    def create_newAllResultsList( pathAllResults : str ):
        if( os.path.isfile(pathAllResults) == False ):
            allResults = list()
            AllResults.saveAsPickle_allResults(allResults, pathAllResults)
        else:
            print( COLORRED + "allResults already exists on given path! Creation of new List aborted. " + COLOREND )


    @staticmethod
    def saveAsPickle_allResults( allResults : List[dict], path : str ):
        with open(path, "wb") as f:
            pickle.dump(allResults, f)


    @staticmethod
    def loadFromPickle_allResults( path : str ) -> pd.DataFrame:
        with open(path, "rb") as f:
            allResults = pickle.load(f)
        return allResults


    @staticmethod
    def showAllResults( input : str | List[dict] ):
        if(type(input) == str):
            allResults = AllResults.loadFromPickle_allResults( input)
        else:
            allResults = input
        for i in range( len(allResults) ):
            print(COLORYELLOW + f"list index = {i}\n" + COLOREND)
            for key in allResults[i]:
                print(COLORCYAN + f"{key} : {allResults[i][key]}" + COLOREND + "\n")


    def getIndices_ofEntriesMatchingCriteria( allResults : List[dict], criteria : dict ): #correct?
        idx_propEntr : List[int] = list( )

        for m in range( len(allResults) ):
            count = 0
            for key in criteria:
                if( criteria[key] == allResults[m][key]):
                    count += 1
                if( count == len(criteria) ):
                    idx_propEntr.append(m)

        if( len( idx_propEntr ) == 0 ):
            print(COLORRED + "No entry in allResults found matching given ccriteria. " + COLOREND)
            sys.exit()

        print("Indices of proper entries: " + COLORGREEN + f"{idx_propEntr}" + COLOREND)
        return idx_propEntr



class AllResultsVolt:
    """ allResultsVolt : List[dict]
                              
        file_id             : str                                = \"participant<>_mainExp<>.vhdr\",                                     
        freqCombCond        : str                                = \"\<fams LMR\>_\<target\>\" #z.B. ABC_left

        recordingElectrodes : List[str]                          = [ \'\<\>\' , \'\<\>\' ]
        referenceElectrodes : List[str] | None | str             = [ \'\<\>\' , \'\<\>\' ] | "average" | None

        filterParams        : tuple[str | int | None]            = (l_freq, h_freq, notch_freq, notch_width)
        ICAParams           : tuple[float | str | int] | None    = (n_componentsICA, methodICA, seed)

        voltageUnit         : str                                = e.g. "V"
        voltageTimes        : tuple[np.ndarray | None]           = (voltage, times)

        # order of recordingElectrodes is perserved inside of 
        # voltage, times, psds, psds_dB and freqs
    """

class AllResultsPower: 
    """ allResultsVolt : List[dict]
                              
        file_id             : str                                = \"participant<>_mainExp<>.vhdr\",                                     
        freqCombCond        : str                                = \"\<fams LMR\>_\<target\>\" #z.B. ABC_left

        recordingElectrodes : List[str]                          = [ \'\<\>\' , \'\<\>\' ]
        referenceElectrodes : List[str] | None | str             = [ \'\<\>\' , \'\<\>\' ] | "average" | None

        filterParams        : tuple[str | int | None]            = (l_freq, h_freq, notch_freq, notch_width)
        ICAParams           : tuple[float | str | int] | None    = (n_componentsICA, methodICA, seed)

        scaling             : str                                = "density" (V^2/Hz) | "spectrum" (V^2)
        psds_freqs          : tuple[np.ndarray]                  = (psds, psds_dB, freqs)

        # order of recordingElectrodes is perserved inside of 
        # voltage, times, psds, psds_dB and freqs
    """   




