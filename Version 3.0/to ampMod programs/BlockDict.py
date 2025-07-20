import json
import random

from Globals import Globals


#class Globals: # Parameter für BlockDicts vom 19.07.2025
#    N_BLOCKS = 72
#    freqCombs = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"] 
#    conditions = ["left", "middle", "right", "both"]



class BlockDict:

    @staticmethod
    def get_pathBlockDict(participantNr):
        # cwd = amplitudeModulation_programs\\V3.0
        return f"\\data\\blockDict\\participant{participantNr}_blockDict.txt" 


    @staticmethod
    def generiere_neuesBlockDict(): #korrekt
        blockDict = dict()
        for i in range( Globals.N_BLOCKS ): ##CAVE
            blockDict[f"block{i}"] = {
                "trial" : None,
                "freqComb" : None,
                "condition" : None
            }
        blockNr = 0
        for trial in [1,2,3]:
            randomisedFreqCombs = Globals.freqCombs.copy()
            random.shuffle( randomisedFreqCombs )

            for freqComb in randomisedFreqCombs:
                randomisedConditions = Globals.conditions.copy()
                random.shuffle( randomisedConditions )

                for condition in randomisedConditions:
                    blockDict[f"block{blockNr}"]["trial"] = trial
                    blockDict[f"block{blockNr}"]["freqComb"] = freqComb
                    blockDict[f"block{blockNr}"]["condition"] = condition
                    blockNr += 1
        return blockDict


    @staticmethod
    def lade_blockDict( pathBlockDict ):
        with open( pathBlockDict, "r" ) as f:
            blockDict = json.load(f)
        return blockDict


    @staticmethod
    def save_blockDict_asJson( blockDict : dict, pathBlockDict : str ):
        with open( pathBlockDict, "w" ) as f:
            json.dump( blockDict, f, indent = 4 )


    #######

    @staticmethod
    def get_pathNrSeqs( participantNr ):
        # cwd = amplitudeModulation_programs\\V3.0
        return f"data\\nrSeqs\\participant{participantNr}_nrSeqs.txt"



# Muss erst neu generiert werden, wenn sich N_BLOCKS ändert:

#participantNr = x
#pathBlockDict = f"data\\blockDict\\participant{participantNr}_blockDict.txt" # cwd = BrainVision Recorder\\Version 3.0
#blockDict = BlockDict.generiere_neuesBlockDict()
#BlockDict.save_blockDict_asJson( blockDict, pathBlockDict)