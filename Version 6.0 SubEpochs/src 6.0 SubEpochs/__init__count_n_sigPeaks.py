from Paths import Paths
from AllResults import AllResults

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



#####
pNr = 1
durchgang = "1"

typ = "threeSpeakers"
#####

pathAllResults_sigPeaks = Paths.get_pathAllResults_sigPeaks(pNr, durchgang, typ)
pathAllResults_snSpeaks = Paths.get_pathAllResults_snSpeaks(pNr, durchgang, typ)

allResults_sigPeaks = AllResults.loadFromPickle_allResults( pathAllResults_sigPeaks )
allResults_snSpeaks = AllResults.loadFromPickle_allResults( pathAllResults_snSpeaks )




for index in range( len(allResults_snSpeaks) ):

    recordingElectrodes = allResults_sigPeaks[index]["recordingElectrodes"]
    referenceElectrodes = allResults_sigPeaks[index]["referenceElectrodes"]

    n_gesPeaks = 0
    for freqCombCond in allResults_snSpeaks[index]["peakDict_snS"]: #1080(24*45)
        for famABC in allResults_snSpeaks[index]["peakDict_snS"][freqCombCond]: #45 (3*15)
            for peak in allResults_snSpeaks[index]["peakDict_snS"][freqCombCond][famABC]: #15
                n_gesPeaks += 1

    n_sigPeaks = 0
    for freqCombCond in allResults_sigPeaks[index]["peakDict_sig"]:
        for famABC in allResults_sigPeaks[index]["peakDict_sig"][freqCombCond]:
            for peak in allResults_sigPeaks[index]["peakDict_sig"][freqCombCond][famABC]:
                n_sigPeaks += 1

    print(COLORYELLOW + f"participant{pNr} " + COLORGREEN + f"index {index} " + COLORRED + f"{recordingElectrodes} VS {referenceElectrodes}" + COLOREND)
    print(n_sigPeaks)
    print(n_gesPeaks)
    print(round( float(n_sigPeaks) / float(n_sigPeaks + n_gesPeaks), 2 ) )


