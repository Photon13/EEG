import mne
import numpy as np
from typing import List
import re

from Roh import Roh
from RohBlock import RohBlock
from Berechnungen import Berechnungen
from Plots import Plots
from Ereignisse import Ereignisse



pathFolder : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\participant0"
pathVHDR : str = pathFolder + "\\maik_pilot0.vhdr"
pathVMRK : str = pathFolder + "\\maik_pilot0.vmrk" 

rawFull = Roh.lade_fullRaw(pathVHDR)
print(rawFull.info)


"""
#     Position     |  Elektrode         |  BVR Channel
#__________________|____________________|_______________
#    leftEar(A1)   |    7 gelb  (=39)   |      F2
#    vertex(Cz)    |    3 gelb  (=35)   |      AF4
#    rightEar(A2)  |    8 gelb  (=40)   |      F6

mapping : dict = {              # old Channel name : new Channel name
    "39"  :  "A1",
    "35"  :  "Cz",
    "40"  :  "A2",   
}
rawFull.rename_channels( 
    mapping = mapping,
    verbose = True
)
picks = ["A1", "Cz", "A2"]      # Channels to keep
bads = rawFull.ch_names.copy()
for ch in picks:
    bads.remove(ch)
rawFull.info["bads"].extend(bads)   # All other channels assigned as bads



refDict : dict = {
    "Cz" : ["A1","A2"]
}
rawFull = mne.set_eeg_reference(    # Replace Channel Cz with Cz - mean(A1,A2)
    rawFull, 
    ref_channels = refDict,
    #ref_channels = ["A1"],
    verbose = True 
)[0]
"""
picks = ["6", "8", "11", "22", "23", "25", "27", "35", "39", "40"]      # Channels to keep
bads = rawFull.ch_names.copy()
for ch in picks:
    bads.remove(ch)
rawFull.info["bads"].extend(bads)   # All other channels assigned as bads


rawFull.plot()
inp = input("any")



with open( pathVMRK, "r" ) as f:
    lines = f.readlines()
for i in range(0,12):
    lines.pop(0)

events_tSampAbs : List[List] = []
for l in lines:
    absTime = int( re.findall( r"\d+", l )[2] )
    markerNr = int( re.findall(r"\d+", l )[1] )
    newEntry = np.array([absTime, 0, markerNr])
    events_tSampAbs.append(newEntry)
events_tSampAbs = np.array(events_tSampAbs) # 3-dimensional array:   e.g. [ [10784 0 161] [11345 0 32] ... ]

event_dict = {
    "zBus" : 65,
    "shiftLeft" : 32,
    "shiftMiddle" : 2,         
    "shiftRight" : 1,
    "button" : 128
}
zBusses : List[int] = []
for i in range( len(events_tSampAbs) ):             
    if( events_tSampAbs[i][2] == 65 ):
        zBusses.append( events_tSampAbs[i][0] )



blockNr = 3
blockLength = 50 # mean length = 60 sec

start = float( zBusses[ blockNr ] ) / float( rawFull.info["sfreq"] )
end = start + blockLength
rawBlock = rawFull.copy().crop( tmin = start, tmax = end )

psds, psds_dB, freqs  = Berechnungen.get_psds( rawBlock, blockLength )
Plots.plot_PSD(psds_dB, freqs)


