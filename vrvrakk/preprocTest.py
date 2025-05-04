from pathlib import Path
import os
from typing import List
from typing import Pattern

import re
from re import Pattern
import matplotlib.pyplot as plt
import numpy as np

import mne
import mne_bids
from mne_bids import copyfiles
from mne_bids.copyfiles import copyfile_brainvision

class PreprocTest:
    # BRAINVISION RECORDER files:
    #       .eeg                    # binary
    #       .vhdr = header file     # text
    #       .vmrk = marker file     # text

    # text files:
    #       comments:           ; <something>
    #       sections:           [ <something> ]
    #       key-value pairs:    <key> = <value>

    # read BrainVision EEG files:
    #       mne.io.read_raw_brainvision(<vhdr full path>) 

    # change reference channel
    #       <new re-referenced raw> = mne.set_eeg_reference( 
    #                                   <raw>, ref_channels = [<>] )
    #
    #       single reference: 
    #               e.g. mne.set_eeg_reference( 
    #                       <raw>, ref_channels = ['A1'] )
    #       average of multiple references: 
    #               e.g. mne.set_eeg_reference( 
    #                       <raw>, ref_channels = ['M1', 'M2'] )
    #
    #       bipolar reference: 
    #               e.g. mne.set_bipolar_reference (
    #                       <raw>, anode = ['F3'], cathode = ['F4'])

    pathCwd = Path(os.getcwd()) # .../vrvrakk
    pathBVR = pathCwd / "BVR_vrvrakk"
    pathFif = pathCwd / "fif_vrvrakk"

    #
    #
    #
    @staticmethod
    def get_searchPattern_vhdr( participantName : str, condition : str) -> Pattern[str]:
        """ Help method for get_properFileDict_raw() """

        searchPattern = re.compile(rf" {participantName}  (_{condition})  (_\d)*  \.vhdr ", re.VERBOSE)
        return searchPattern


    @staticmethod
    def get_headerFiles(participantName : str, condition : str) -> List[str]:

        dirList : List[str] = os.listdir(PreprocTest.pathBVR)
        fileList : List[str] = []
        for entry in dirList:
            if os.path.isfile(PreprocTest.pathBVR / entry) == True:
                fileList.append(entry)

        searchPatternDict_vhdr = PreprocTest.get_searchPattern_vhdr( participantName, condition)
        
        vhdrFileList : List[str] = []
        for fileName in fileList:
            if( re.search(searchPatternDict_vhdr, fileName) != None):
                vhdrFileList.append(fileName)

        return vhdrFileList # only name.extension


    def rawToFif(participantName : str, condition : str) -> None:

        headerFileList : List[str] = PreprocTest.get_headerFiles(participantName, condition)
        headerFileList_longPath : List[Path] = []

        for entry in headerFileList:
            longEntry = PreprocTest.pathBVR / entry
            headerFileList_longPath.append(longEntry)

        dict = {}
        for i in range(len(headerFileList)):
            
            dict[f"file{i}"] = mne.io.read_raw_brainvision(headerFileList_longPath[i])
        
        rawList : List = []
        for value in dict.values():
            rawList.append(value)
        rawList : List 

        if( len(headerFileList) > 1):
            raw = mne.concatenate_raws(rawList)
        else:
            raw = rawList[0]
        # funzt bis hier


        ### TO ADD:  set montage etc. on raw

        savepath = PreprocTest.pathFif / f"{participantName}_{condition}.fif"
        raw.save(savepath)

"""
    raw = mne.io.read_raw_brainvision(headerFile)
    # XOR
    raw = mne.concatenate_raws(headerFileList)

    mne.set_eeg_reference(raw)
    # XOR
    raw.set_eeg_reference()

    pathFileFif : Path = Path(os.getcwd()) / 
    <raw fif> = mne.io.read_raw_fif(pathFileFif)

    mne.preprocessing
    from mne.preprocessing import ICA, corrmap, create_ecg_epochs, create_eog_epochs
    
    
    
    mne.filter

    # ICA(Independent Component Analysis)
    #       -> Repair of artefacts
    # algorithm e.g. picard


    <raw fif>.compute_psd(fmax = <low_pass_f + 10 Hz>).plot() # power spectrum
    <raw fif>.plot()

"""


class HelperMethodsPreprocTest:

    def rename_BVRfiles(folderPath : Path, oldFileName : str, newFileName):
        """ Copies files and saves them with new name and references to each other \n
                Old name and new name  WITHOUT extension \n
                FolderPath is path to raw files """
        
        oldFilePath = folderPath / f"{oldFileName}.vhdr"
        newFilePath = folderPath / f"{newFileName}.vhdr"
        copyfiles.copyfile_brainvision(oldFilePath, newFilePath) 



# MAIN:
PreprocTest.rawToFif(participantName = "ad", condition = "a1")