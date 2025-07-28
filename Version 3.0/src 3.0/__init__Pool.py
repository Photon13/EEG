from Normierung import Normierung
from BlockParams import BlockParams
from RohBlock import RohBlock
from Paths import Paths
from Roh import Roh
from RohBlock import RohBlock
from Berechnungen import Berechnungen
from HelpMethods import HelpMethods

import json
import mne
from typing import List
import copy


COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


def mainPool():
    # TEILNEHMER DATEN:
    pNr = 13                        # <---
    #durchgang = ""                 
    durchgang = "3" #MonkeyPatch    # <---

    # PFADE:
    pathVHDR, pathVMRK, pathBlockDict = Paths.get_paths(pNr, durchgang)

    # PARAMETER:
    blockLength  = BlockParams.BLOCK_LENGTH 
    n_blocks     = BlockParams.N_BLOCKS
    famA = BlockParams.FAM_A
    famB = BlockParams.FAM_B
    famC = BlockParams.FAM_C

    fABC = BlockParams.F_ABC
    #fABC = [33.0, 43.0, 53.0] #MonkeyPatch     # <---


    badBlocks : List[str] = []                          # <---
        # z.B. ["block3", "block5"] oder leere Liste
        # Tipp: rawFull durchscrollen

    #############################################################################################################################################

    # LADE RAW FULL:
    rawFull = Roh.lade_fullRaw( pathVHDR )
    rawFull = Roh.assign_unusedChannels_asBads( rawFull )

    rawFull = mne.set_eeg_reference( 
        rawFull, 
        ref_channels = {
            "14" : ["13", "15"]  # <---
        }, 
        verbose = True )[0]


    #############################################################################################################################################
    
    # ERSTELLUNG DICT UM P_fLMR-WERTE DER BLÖCKE NACH KONDITION UND FREQCOMB ZU SORTIEREN:
    P_fLMR_dict = dict()
    for target in BlockParams.conditions:
        P_fLMR_dict[target] = dict()
        for freqComb in BlockParams.freqCombs:
            P_fLMR_dict[target][freqComb] = [[], [], []]
            

    # ITERATION DURCH ALLE BLÖCKE:
    for blockNr in range(n_blocks):

        # ERZEUGE RAW FÜR BESTIMMTEN BLOCK:
        start, end = RohBlock.getBlockStartAndEnd( blockNr, rawFull.info["sfreq"], blockLength, pathVMRK )
        rawBlock = rawFull.copy().crop( tmin = start, tmax = end )

        # ABRUF BLOCK-DATEN:
        with open( pathBlockDict, "r" ) as f:
            blockDict = json.load(f)

        trial     = blockDict[f"block{blockNr}"]["trial"] 
        freqComb  = blockDict[f"block{blockNr}"]["freqComb"]
        target    = blockDict[f"block{blockNr}"]["condition"]

        
        # BERECHNE PSD_WERTE FÜR SPEZIFIZIERTEN BLOCK:
        psds, psds_dB, freqs  = Berechnungen.get_psds( rawBlock, blockLength )

        f_ABC  = [BlockParams.FAM_A, BlockParams.FAM_B, BlockParams.FAM_C]
        P_fABC = Berechnungen.berechnePower_P_fABC( fABC, freqs , psds_dB , border = 1.0  )
        P_fLMR = Berechnungen.bestimme_P_fLMR( freqComb, P_fABC )
        
        print(P_fLMR)
        P_fLMR_dict[target][freqComb][trial-1] = list(P_fLMR)
            # P_fLMR_dict[target][freqComb] = [ [<trial1>], [<trial2>], [<trial3>] ]
        print(P_fLMR_dict[target][freqComb])



    # BERECHNE DURCHSCHNITTLICHE PSD ÜBER ALLE TRIALS:
    P_mean_fLMR_dict = copy.deepcopy(P_fLMR_dict) 
        #.copy() does not work-> dict entries are not newly created and therefore going to be overridden

    for target in BlockParams.conditions:
        for freqComb in BlockParams.freqCombs:
            lst = P_mean_fLMR_dict[target][freqComb]
            linkeEintraege = []
            mittlereEintraege = []
            rechteEintraege = []

            for tr in range( len( lst) ):
                linkeEintraege.append(    lst[tr][0] )
                mittlereEintraege.append( lst[tr][1] )
                rechteEintraege.append(   lst[tr][2] )


            mean_links  = HelpMethods.berechne_meanEintraege( linkeEintraege )
            mean_mitte  = HelpMethods.berechne_meanEintraege( mittlereEintraege )
            mean_rechts = HelpMethods.berechne_meanEintraege( rechteEintraege )

            P_mean_fLMR_dict[target][freqComb] = [mean_links, mean_mitte, mean_rechts] 
                # stimmt



            # BERECHNE P_TARGET UND P_NONTARGET:
            P_fTNT_dict = copy.deepcopy(P_fLMR_dict)


            # ...

            return P_mean_fLMR_dict
    


"""
Anwendungsbeispiel:
-------------------

print( P_mean_fLMR_dict["left"]["ABC"] )    # printet [ P_Links, P_Mitte, P_Rechts ] für target = links, freqComb = ABC
                                            # P_<> hier jeweils Durchschnitt aller trials 
                                            # (excl. als chlecht deklarierte schlechte Blöcke)
"""

P_mean_fLMR_dict = mainPool()