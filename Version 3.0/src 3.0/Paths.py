class Paths:

    @staticmethod
    def get_paths(participantNr : int, durchgang :str):
        pathCWD   = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder\\Version 3.0"
        folderEEG = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"

        pathVHDR  = folderEEG + f"\\participant{participantNr}\\participant{participantNr}_mainExp{durchgang}.vhdr"
        pathVMRK  = folderEEG + f"\\participant{participantNr}\\participant{participantNr}_mainExp{durchgang}.vmrk"
        pathBlockDict = f"data\\blockDict\\participant{participantNr}_blockDict.txt"

        return pathVHDR, pathVMRK, pathBlockDict