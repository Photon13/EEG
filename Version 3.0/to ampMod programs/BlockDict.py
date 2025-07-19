import json
import random

class BlockDict:

    @staticmethod
    def get_pathBlockDict(participantNr):
        # cwd = amplitudeModulation_programs\\V3.0
        return f"\\data\\blockDict\\participant{participantNr}_blockDict" 


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
        jsonObj = json.dump( blockDict )
        with open( pathBlockDict, "w" ) as f:
            f.write( jsonObj )

    #######

    @staticmethod
    def get_pathNrSeqs( participantNr ):
        # cwd = amplitudeModulation_programs\\V3.0
        return f"\\data\\nrSeqs\\participant{participantNr}_nrSeqs"

#blockDict = BlockDict.generiere_neuesBlockDict()
#pathBlockDict = "\\data\\blockDict" # amplitudeModulation_programs\\V3.0
#BlockDict.save_blockDict_asJson( blockDict, BlockDict.pathBlockDict )




