from BlockDict import BlockDict
from Fams import Fams

import time
import json
from typing import List


version 2.1

##
N_BLOCKS = 72 !
BLOCK_LENGTH = 30 !
freqCombs = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"] !
conditions = ["left", "middle", "right", "both"] !
-> Globals

Ordner erstellen für blockDict und nrseqs !!!
BlockDict pre-generieren !
##





@staticmethod
def main_new():

    pNr = 0                 # <--
    pathBlockDict =  BlockDict.get_pathBlockDict( pNr ) 
    pathNrSeqs = BlockDict.get_pathBlockDict( pNr )

    ampRise = 0.3


    while True:
        inp = input(Globals.COLORRED + "Remember to start recording! " + Globals.COLORCYAN + "Start? [yes]: " + Globals.COLOREND)
        if( inp.lower() == "yes"):
            break

    Sprecher_und_Procs.initFF()
    speakers, leds = Sprecher_und_Procs.pickSpeakersAndLeds()

    blockDict = BlockDict.lade_blockDict( pathBlockDict )

    count = 0 
    for i in range( len(blockDict) ):
        target = blockDict[f"block{i}"]["condition"]
        freqComb = blockDict[f"block{i}"]["freqComb"]
        famsLMR : List[float] = Fams.get_fams_fromFreqComb( freqComb )
        # 
        nrSeqsLMR : List[List] = Generator.generate_nrSeqs_mainExp(ampRise)
        with open( pathNrSeqs, "a" ) as f:
            f.write(   f"nrSeqLeft = {nrSeqsLMR[0]}\n"   ) # einfach nur reinmüllen
            f.write( f"nrSeqMiddle = {nrSeqsLMR[1]}\n"   )
            f.write(  f"nrSeqRight = {nrSeqsLMR[2]}\n\n" )

        Sprecher_und_Procs.turnTargetLedOn(leds, target)
        time.sleep(3)

        Sprecher_und_Procs.writeToSpeaker( "left",   speakers, famsLMR, nrSeqsLMR[0]   )
        Sprecher_und_Procs.writeToSpeaker( "middle", speakers, famsLMR, nrSeqsLMR[1] )
        Sprecher_und_Procs.writeToSpeaker( "right",  speakers, famsLMR, nrSeqsLMR[2]  )

        freefield.play()
        time.sleep( len( nrSeqsLMR[0]) )   
    
    
        count += 1 
        if( count == 4): # n blocks nach denen Pause auftreten soll
            while True:
                inp = input("Continue? [yes]: ")
                if( inp.lower() == "yes"):
                    break
            count = 0
   
        Sprecher_und_Procs.turnAllLedsOff(leds)
        time.sleep(3) # zeitlicher Puffer bevor nächste Daten geladen werden
            

    freefield.halt()  
    print(blockDict)

##############################################################################################################################################

main_new()


