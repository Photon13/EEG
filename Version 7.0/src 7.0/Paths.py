class Paths:

    @staticmethod
    def get_basisPath(expType):
        """ typ = \"threeSpeakers\" | \"singleSpeaker\" """
        basisPath = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results 7.0"
        return basisPath
    
    @staticmethod
    def get_endingFileName_perTyp(pNr, durchgang, expType):
        if( expType == "threeSpeakers" ):
            return f"participant{pNr}_mainExp{durchgang}"
        elif( expType == "singleSpeaker" ):
            return f"participant{pNr}_singleSpeaker"

    @staticmethod  
    def get_pathAllResults(pNr, durchgang, expType):
        basisPath      = Paths.get_basisPath(expType)
        pathAllResults = basisPath + f"\\allResults\\allResults_{Paths.get_endingFileName_perTyp(pNr, durchgang, expType)}.pkl" 
        print(pathAllResults)
        return pathAllResults