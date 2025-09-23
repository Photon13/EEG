import re
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


def get_markersTimes_andBlockDict(pNr, durchgang):

    folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"
    file_id = f"participant{pNr}_mainExp{durchgang}"

    pathVMRK  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vmrk"
    pathBlockDict   = f"data\\blockDict\\participant{pNr}_blockDict.txt"

    with open( pathBlockDict, "r" ) as f:
        blockDict : dict[dict] = json.load(f)

    with open(pathVMRK, "r") as f:
        vmrk_lines : List[str] = f.readlines()
    
    for i in range(0,12):
        vmrk_lines.pop(0)

    tSampAbs_perMarker : dict = {
        "S161" : [],
        "S 32" : [],
        "S  2" : [],
        "S 34" : [],
        "S128" : []
    }
    for line in vmrk_lines:
        marker  = re.findall( r"S\s{0,3}\d{1,3}", line )[0]
        absTime = re.findall( r"\d+", line )[2]
        tSampAbs_perMarker[f"{marker}"].append( int(absTime) )

    tSampAbs_perMarker["zBus"]        = tSampAbs_perMarker["S161"]
    tSampAbs_perMarker["shiftLeft"]   = tSampAbs_perMarker["S 32"]
    tSampAbs_perMarker["shiftMiddle"] = tSampAbs_perMarker["S  2"]
    tSampAbs_perMarker["shiftRight"]  = tSampAbs_perMarker["S 34"]
    tSampAbs_perMarker["button"]      = tSampAbs_perMarker["S128"]

    del tSampAbs_perMarker["S161"]
    del tSampAbs_perMarker["S 32"]
    del tSampAbs_perMarker["S  2"]
    del tSampAbs_perMarker["S 34"]
    del tSampAbs_perMarker["S128"]

    return tSampAbs_perMarker, blockDict


def printButtonPressAnalysis(pNr, durchgang):
    tSampAbs_perMarker, blockDict = get_markersTimes_andBlockDict(pNr, durchgang)  
    #print(tSampAbs_perMarker)

    shiftCountDict = {}
    for shiftType in ["shiftLeft", "shiftMiddle", "shiftRight"]:
        shiftCountDict[shiftType] = {
            "left"   : 0,
            "middle" : 0,
            "right"  : 0,
            "both"   : 0
        }
    buttonCountDict = {}
    for pressType in ["shiftLeft", "shiftMiddle", "shiftRight"]: #press after shift at position x
        buttonCountDict[pressType] = {
            "left"   : 0,
            "middle" : 0,
            "right"  : 0,
            "both"   : 0
        }

    for i in range(72): #72
        condition  : str = blockDict[f"block{i}"]["condition"]
        blockStart : int   = tSampAbs_perMarker["zBus"][i]      #[samples]
        blockEnd   : int   = blockStart + (30*500)              #[samples]

        for shiftType in ["shiftLeft", "shiftMiddle", "shiftRight"]:
            for shift in tSampAbs_perMarker[shiftType]:
                if( blockStart < shift < blockEnd ):    #if shift belongs to block
                    shiftCountDict[shiftType][condition] += 1
                    if any (shift <= button <= shift + 500 for button in tSampAbs_perMarker["button"]): # if any button press occurred between 0 sec and 2 sec after shift
                        buttonCountDict[shiftType][condition] += 1

    relationDict = {}
    for shiftType in shiftCountDict:
        relationDict[shiftType] = {}
        for cond in shiftCountDict[shiftType]:
            relation = float(buttonCountDict[shiftType][cond]) / float(shiftCountDict[shiftType][cond])
            relationDict[shiftType][cond] = round(100 *relation, 1)

    print(COLORPURPLE + f"participant{pNr}" + COLOREND)
    dicts = [shiftCountDict, buttonCountDict, relationDict]
    dictNames = ["shiftCountDict", "buttonCountDict", "relationDict"]
    colours = [COLORGREEN, COLORRED, COLORCYAN]
    
    for i in range(3):
        print(colours[i] + f"\n---{dictNames[i]}---")
        for cond in ["left", "middle", "right", "both"]:
            print("\n")
            for shiftPos in ["shiftLeft", "shiftMiddle", "shiftRight"]:
                print( f"{cond} {shiftPos} {dicts[i][shiftPos][cond]}")
        print(COLOREND)





identifiers = [                     # <---
    [13, "3"],
    #[4, "4"],
    #[3, "3"],
    #[2, "2"],
    #[1, "1"],
]


for idNr in range(len(identifiers)):
    pNr       = identifiers[idNr][0]
    durchgang = identifiers[idNr][1] 
    printButtonPressAnalysis(pNr, durchgang)
    
    
                
