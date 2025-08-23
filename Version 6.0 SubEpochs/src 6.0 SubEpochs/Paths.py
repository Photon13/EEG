class Paths:

    def get_basisPath(typ):
        """ typ = \"threeSpeakers\" | \"singleSpeaker\" """
        basisPath = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results SubEpochs"
        if( typ == "threeSpeakers" ):
            basisPath = basisPath + "\\allResultsSubEpochs\\"
        elif( typ == "singleSpeaker" ): 
            basisPath = basisPath + "\\allResultsSubEpochs_singleSpeaker\\"
        return basisPath
    
    def get_endingFileName_perTyp(pNr, durchgang, typ):
        if( typ == "threeSpeakers" ):
            return f"participant{pNr}_mainExp{durchgang}"
        elif( typ == "singleSpeaker" ):
            return f"participant{pNr}_singleSpeaker"
    
    def get_pathAllResultsVolt(pNr, durchgang, typ):
        basisPath          = Paths.get_basisPath(typ)
        pathAllResultsVolt = basisPath + f"allResultsVolt\\allResultsVolt_{Paths.get_endingFileName_perTyp(pNr, durchgang, typ)}.pkl" 
        print(pathAllResultsVolt)
        return pathAllResultsVolt
    
    def get_pathAllResultsPSD(pNr, durchgang, typ):
        basisPath          = Paths.get_basisPath(typ)
        pathAllResultsPSD  = basisPath + f"allResultsPSD\\allResultsPSD_{Paths.get_endingFileName_perTyp(pNr, durchgang, typ)}.pkl"
        return pathAllResultsPSD
    
    def get_pathAllResults_sigPeaks(pNr, durchgang, typ):
        basisPath                = Paths.get_basisPath(typ)
        pathAllResults_sigPeaks  = basisPath + f"allResults_sigPeaks\\allResults_sigPeaks_{Paths.get_endingFileName_perTyp(pNr, durchgang, typ)}.pkl"
        return pathAllResults_sigPeaks
    
    def get_pathAllResults_snSpeaks(pNr, durchgang, typ):
        basisPath                = Paths.get_basisPath(typ)
        pathAllResults_snSpeaks  = basisPath + f"allResults_snSpeaks\\allResults_snSpeaks_{Paths.get_endingFileName_perTyp(pNr, durchgang, typ)}.pkl"
        return pathAllResults_snSpeaks