class Paths:

    def get_basisPath():
        basisPath = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\Results SubEpochs\\allResultsSubEpochs\\"
        return basisPath
    
    def get_pathAllResultsSubEpochsVolt(pNr, durchgang):
        basisPath = Paths.get_basisPath()
        pathAllResultsEpochsVolt = basisPath + f"allResultsEpochsVolt\\allResultsEpochsVolt_participant{pNr}_mainExp{durchgang}.pkl" 
        return pathAllResultsEpochsVolt
    
    def get_pathAllResultsSubEpochsPSD(pNr, durchgang):
        basisPath = Paths.get_basisPath()
        pathAllResultsSubEpochsPSD  = basisPath + f"allResultsEpochsPSD\\allResultsEpochsPSD_participant{pNr}_mainExp{durchgang}.pkl"
        return pathAllResultsSubEpochsPSD
    
    def get_pathAllResults_sigPeaks(pNr, durchgang):
        basisPath = Paths.get_basisPath()
        pathAllResults_sigPeaks  = basisPath + f"allResults_sigPeaks\\allResults_sigPeaks_participant{pNr}_mainExp{durchgang}.pkl"
        return pathAllResults_sigPeaks
    
    def get_pathAllResults_snSpeaks(pNr, durchgang):
        basisPath = Paths.get_basisPath()
        pathAllResults_snSpeaks  = basisPath + f"allResults_snSpeaks\\allResults_snSpeaks_participant{pNr}_mainExp{durchgang}.pkl"
        return pathAllResults_snSpeaks