# Daten vom labPC nicht auf GITHUB!
# Daten müssen vom labPC gepusht werden.
#
# Kein marker für MITTLEREN SHIFT vorhanden!
# Gesamtzahl shifts stimmt aber (24*16 = 284) s. raw.annotations
# Entweder zufällig keine mittleren shifts
#   (Shifts wurden aber scheinbar in der mitte gehört (??))
# oder statt marker mitte wurde einer der anderen beiden gesendet (z.B. 34)
#   ->shiftMitte im BlockDict vorhanden?
#
#
# TARGETLISTEN erneuern! Die TargetListen sind 20 Blöcke lang, sollten aber nur 16 Blöcke lang sein.
# Main ist korrekt, Generator ist auch korrekt. Es müssen lediglich neue Listen generiert werden zum Ersetzen der alten in ParticipantConstants.

import mne
import numpy as np

from typing import List
import re

from Mne_EEGAnalyse import Mne_EEGAnalyse
from Computations import Computations
from Plots import Plots


COLORRED    = '\33[31m'
COLORCYAN = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN = "\033[0;32m"
COLOREND = '\033[0m'




##############
pNr   = 0    #      #participantNr
blockDuration : int = 96             #
##############
                                                                                
##############
targetList : List[str] = ['middle', 'left', 'right', 'both', 'both', 'left', 'both', 'both', 'right', 'both', 'left', 'right', 'right', 'left', 'middle', 'left']
rest = ['middle', 'right', 'middle', 'middle'] # CAVE: letzte 4 Blöcke wurden bei participant0 nicht gespielt
##############




folderEEG = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"
pathVHDR = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp1.vhdr"
pathVMRK = folderEEG + f"\\participant{pNr}\\participant{pNr}_mainExp1.vmrk"

#path_cwd = BrainVision Recorder
pathTargetList = f"data\\participant{pNr}\\targetList_participant{pNr}.txt"
#pathAnnotations = f"data\\participant{pNr}\\annotations_participant{pNr}.txt"




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# GET RAWS:
#~~~~~~~~~~~

"""
rawFull = Mne_EEGAnalyse.get_raw(pathVHDR, renamedChannels=True, reReferencing=True, filtering=False )
"""


raws_concatenatedLeft   = Mne_EEGAnalyse.get_croppedRaw( pathVHDR, pathVMRK, targetList, blockDuration, target="left", renamedChannels=True, reReferencing=True, filtering=False )

raws_concatenatedMiddle = Mne_EEGAnalyse.get_croppedRaw( pathVHDR, pathVMRK, targetList, blockDuration, target="middle", renamedChannels=True, reReferencing=True, filtering=False )

raws_concatenatedRight  = Mne_EEGAnalyse.get_croppedRaw( pathVHDR, pathVMRK, targetList, blockDuration, target="right", renamedChannels=True, reReferencing=True, filtering=False )
raws_concatenatedBoth   = Mne_EEGAnalyse.get_croppedRaw( pathVHDR, pathVMRK, targetList, blockDuration, target="both", renamedChannels=True, reReferencing=True, filtering=False )         



### EVT BOUNDARIES DER EINZEL-RAWS ALS BADS EINSTELLEN?
### Auto-Reject?


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DEFINE BAD INTERVALLS:
#~~~~~~~~~~~~~~~~~~~~~~~                    

"""                                                            
annotationsLeft = mne.Annotations(          # block1: heavily moved
    onset = [0.0], 
    duration = [blockDuration], 
    description = ["bad_movement"] 
) 
raws_concatenatedLeft.set_annotations(annotationsLeft)                      #CAVE set_annotations() overides all annotations!



annotationsMiddle= mne.Annotations(         # block0: heavily moved
    onset = [0.0], 
    duration = [blockDuration], 
    description = ["bad_movement"] ) 

raws_concatenatedMiddle.set_annotations(annotationsMiddle)
"""


### SAVE ANNOTATIONS IN TXT?


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# PLOTTING:
#~~~~~~~~~~

"""
Plots.plotMarkers_perTime(rawFull, pathVMRK)

#Plot.plot_evokedPotentials(raws_concatenatedLeft, pathVMRK, "shiftLeft")



spectrum = raws_concatenatedLeft.compute_psd( 
    "welch",
    #fmin=fmin,
    #fmax=fmax,
    picks = "Cz",
    reject_by_annotation = True,
    verbose=True,
)
#spectrum.plot()
#inp = input("any ")

psd, freqs = spectrum.get_data(return_freqs=True)
Plots.plot_PSD(psd, freqs)

#snr = Computations.snrSpektrumNEU(psd, n_includePerSide=1, n_skipPerSide=1)
#Plots.plot_SNR(snr, freqs)
"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tmin, tmax = -1.0, 20.0
epochs = mne.Epochs(
    raws_concatenatedRight,
    tmin=tmin,
    tmax=tmax,
    baseline=None,
    verbose=False,
)
tmin = 1.0
tmax = 20.0
fmin = 1.0
fmax = 90.0
sfreq = epochs.info["sfreq"]

spectrum = epochs.compute_psd(
    "welch",
    n_fft=int(sfreq * (tmax - tmin)),
    n_overlap=0,
    n_per_seg=None,
    tmin=tmin,
    tmax=tmax,
    picks = "Cz",
    fmin=fmin,
    fmax=fmax,
    window="boxcar",
    verbose=True,
)



psd, freqs = spectrum.get_data(return_freqs=True)
#Plots.plot_PSD(psd, freqs)
snr = Computations.snr_spectrum(psd, 1, 1)
snr.plot(freqs, snr)

fig, axes = plt.subplots(2, 1, sharex="all", sharey="none", figsize=(8, 5))
freq_range = range(
    np.where(np.floor(freqs) == 1.0)[0][0], np.where(np.ceil(freqs) == fmax - 1)[0][0]
)

psds_plot = 10 * np.log10(psds)
psds_mean = psds_plot.mean(axis=(0, 1))[freq_range]
psds_std = psds_plot.std(axis=(0, 1))[freq_range]
axes[0].plot(freqs[freq_range], psds_mean, color="b")
axes[0].fill_between(
    freqs[freq_range], psds_mean - psds_std, psds_mean + psds_std, color="b", alpha=0.2
)
axes[0].set(title="PSD spectrum", ylabel="Power Spectral Density [dB]")

# SNR spectrum
snr_mean = snrs.mean(axis=(0, 1))[freq_range]
snr_std = snrs.std(axis=(0, 1))[freq_range]

axes[1].plot(freqs[freq_range], snr_mean, color="r")
axes[1].fill_between(
    freqs[freq_range], snr_mean - snr_std, snr_mean + snr_std, color="r", alpha=0.2
)
axes[1].set(
    title="SNR spectrum",
    xlabel="Frequency [Hz]",
    ylabel="SNR",
    ylim=[-2, 30],
    xlim=[fmin, fmax],
)
fig.show()