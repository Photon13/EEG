import mne
from pathlib import Path
import os
import numpy as np
from autoreject import AutoReject, Ransac
from collections import Counter
import json
from meegkit import dss
from matplotlib import pyplot as plt, patches

import re
from typing import List


COLORBLUE = '\33[34m'
COLORGREEN = "\033[0;32m"
COLORRED = '\33[31m'
COLOREND = '\033[0m'

class PreprocTest:

    @staticmethod
    def get_fileList(pathFolder : Path) -> List[str]:
        
        dirList : List[str] = os.listdir(pathFolder)
        fileList : List[str] = []

        for entry in dirList:
            if os.path.isfile(pathFolder / entry) == True:
                fileList.append(entry)
        return fileList

    @staticmethod
    def get_properFileList(searchPattern : str, pathFolder : Path) -> List[str]:

        fileList : List[str] = PreprocTest.get_fileList(pathFolder)
        properFileList : List[str] = []
        
        for fileName in fileList:
            if( re.search(searchPattern, fileName) != None):
                properFileList.append(fileName)
        return properFileList

    @staticmethod
    def load_jsonSettings():
        with open(PreprocTest.pathJson_eeg_events) as file:
            markersDict = json.load(file)

        with open(PreprocTest.pathJson_electrode_names) as file:
            mappingElectrodes = json.load(file)

        with open(PreprocTest.pathJson_preproc_config) as file:
            configuration = json.load(file)
        return markersDict, mappingElectrodes, configuration

    @staticmethod
    def get_searchPatternDict_raw( participantName : str, extension : str) -> dict:
        searchPattern_a1 = re.compile(rf" {participantName}  (_a1)  (_\d)*  {extension} ", re.VERBOSE)
        searchPattern_a2 = re.compile(rf" {participantName}  (_a2)  (_\d)*  {extension} ", re.VERBOSE)
        searchPattern_e1 = re.compile(rf" {participantName}  (_e1)  (_\d)*  {extension} ", re.VERBOSE)
        searchPattern_e2 = re.compile(rf" {participantName}  (_e2)  (_\d)*  {extension} ", re.VERBOSE)

        searchPatternDict_raw : dict= {
            "searchPattern_a1" : searchPattern_a1,
            "searchPattern_a2" : searchPattern_a2,
            "searchPattern_e1" : searchPattern_e1,
            "searchPattern_e2" : searchPattern_e2
        }
        return searchPatternDict_raw

    def get_properFileDict_raw(participantName : str) -> dict:
        searchPatternDict_eeg = PreprocTest.get_searchPatternDict_raw(participantName, ".eeg")
        searchPatternDict_vhdr = PreprocTest.get_searchPatternDict_raw(participantName, ".vhdr")
        searchPatternDict_vmrk = PreprocTest.get_searchPatternDict_raw(participantName, ".vmrk")


        eegFiles_a1 : List[str] = PreprocTest.get_properFileList(searchPatternDict_eeg["searchPattern_a1"],  PreprocTest.pathRawFolder)
        eegFiles_a2 : List[str] = PreprocTest.get_properFileList(searchPatternDict_eeg["searchPattern_a2"],  PreprocTest.pathRawFolder)
        eegFiles_e1 : List[str] = PreprocTest.get_properFileList(searchPatternDict_eeg["searchPattern_e1"],  PreprocTest.pathRawFolder)
        eegFiles_e2 : List[str] = PreprocTest.get_properFileList(searchPatternDict_eeg["searchPattern_e2"],  PreprocTest.pathRawFolder)

        vhdrFiles_a1 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vhdr["searchPattern_a1"],  PreprocTest.pathRawFolder)
        vhdrFiles_a2 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vhdr["searchPattern_a2"],  PreprocTest.pathRawFolder)
        vhdrFiles_e1 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vhdr["searchPattern_e1"],  PreprocTest.pathRawFolder)
        vhdrFiles_e2 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vhdr["searchPattern_e2"],  PreprocTest.pathRawFolder)

        vmrkFiles_a1 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vmrk["searchPattern_a1"],  PreprocTest.pathRawFolder)
        vmrkFiles_a2 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vmrk["searchPattern_a2"],  PreprocTest.pathRawFolder)
        vmrkFiles_e1 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vmrk["searchPattern_e1"],  PreprocTest.pathRawFolder)
        vmrkFiles_e2 : List[str] = PreprocTest.get_properFileList(searchPatternDict_vmrk["searchPattern_e2"],  PreprocTest.pathRawFolder)
    
        properFileDict_raw : dict = {
            "eegFiles_a1" : eegFiles_a1,
            "eegFiles_a2" : eegFiles_a2,
            "eegFiles_e1" : eegFiles_e1,
            "eegFiles_e2" : eegFiles_e2,

            "vhdrFiles_a1" : vhdrFiles_a1,
            "vhdrFiles_a2" : vhdrFiles_a2,
            "vhdrFiles_e1" : vhdrFiles_e1,
            "vhdrFiles_e2" : vhdrFiles_e2,
            
            "vmrkFiles_a1" : vmrkFiles_a1,
            "vmrkFiles_a2" : vmrkFiles_a2,
            "vmrkFiles_e1" : vmrkFiles_e1,
            "vmrkFiles_e2" : vmrkFiles_e2
        }
        return properFileDict_raw
    

    @staticmethod
    def load_concatenatedMneFileVhdr(loadPath : Path):
        concatenatedMneFileVhdr = mne.io.read_raw_brainvision(loadPath, preload=True)
        return concatenatedMneFileVhdr


    @staticmethod
    def get_concatenatedMneFileVhdr(participantName : str, condition : str, properFileDict_raw : dict,  mappingElectrodes):
        """ condition: a1 XOR a2 XOR e1 XOR e2 """
        
        fifPath = PreprocTest.get_savePath_concatenatedMneFileVhdr(participantName, condition)
        if(fifPath.exists() == True):
            print(COLORRED + ".fif already exists. " + COLORBLUE + "Loading old .fif" + COLOREND)
            concatenatedMneFileVhdr = PreprocTest.load_concatenatedMneFileVhdr(fifPath)
            return concatenatedMneFileVhdr

        vhdrList = properFileDict_raw[f"vhdrFiles_{condition}"]

        mneFilesVhdr : List[str] = [] 
        for entry in vhdrList:
            longStrPath = f"{str(PreprocTest.pathRawFolder)}\\{entry}"
            mneFileLongPath = mne.io.read_raw_brainvision(longStrPath)
            mneFilesVhdr.append(mneFileLongPath)

        concatenatedMneFileVhdr = mne.concatenate_raws(mneFilesVhdr)

        concatenatedMneFileVhdr.rename_channels(mappingElectrodes)
        concatenatedMneFileVhdr.set_montage('standard_1020') # ?
        concatenatedMneFileVhdr.save(fifPath, overwrite = True) # override unnecessary ?

        return concatenatedMneFileVhdr
    

    # LOAD PATHS:
    pathCwd : Path = Path(os.getcwd())
    # amplitudeModulation / BrainVision Recorder / vrvrakk

    pathRawFolder : Path = pathCwd / "raw_vrvrakk"
    pathZwischenFolder : Path = pathCwd / "zwischen_vrvrakk"

    pathJson_eeg_events : Path = pathCwd / "eeg_events.json"
    pathJson_electrode_names : Path = "electrode_names.json"
    pathJson_preproc_config : Path = "preproc_config.json"

    def get_savePath_concatenatedMneFileVhdr(participantName : str, condition : str) -> Path:
        savePath : Path = PreprocTest.pathZwischenFolder / f"{participantName}_{condition}.fif"
        return savePath




markersDict, mappingElectrodes, configuration = PreprocTest.load_jsonSettings()

participantName = "ad"

properFileDict_raw : dict = PreprocTest.get_properFileDict_raw(participantName)
print(properFileDict_raw)

concatenatedMneFileVhdr_a1 = PreprocTest.get_concatenatedMneFileVhdr(participantName, "a1", properFileDict_raw,  mappingElectrodes)
concatenatedMneFileVhdr_a2 = PreprocTest.get_concatenatedMneFileVhdr(participantName, "a2", properFileDict_raw,  mappingElectrodes)
concatenatedMneFileVhdr_e1 = PreprocTest.get_concatenatedMneFileVhdr(participantName, "e1", properFileDict_raw,  mappingElectrodes)
concatenatedMneFileVhdr_e2 = PreprocTest.get_concatenatedMneFileVhdr(participantName, "e2", properFileDict_raw,  mappingElectrodes)


concatenatedMneFileVhdr_a1.drop_channels(['A1', 'A2', 'M2']) # drop EMG channels


s1_events = markersDict["s1_events"]
s2_events = markersDict["s2_events"]
response_events = markersDict["response_events"]

target_events = s1_events

events = mne.events_from_annotations(concatenatedMneFileVhdr_a1)[0]
events = events[[not   entry in [99999]   for entry in events[:, 2]]]  # remove specific events, if in 2. column
events = [entry   for entry in events   if entry[2] in target_events.values()]
events = np.array(events)

concatenatedMneFileVhdr_a1.plot()

###
#condition : str =
###


# misc

# pathResultsFolder

# pathDiagrams # results/figures

# pathEpochs

# pathEvokeds

print(f"CWD : {os.getcwd()}")