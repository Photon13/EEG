from Ereignisse import Ereignisse
from BlockParams import BlockParams

from AllResults import AllResults
from Paths import Paths
from Plots import Plots

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import os

import mne
import copy

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'



recordingElectrodes = ["25"]               # <---
referenceElectrodes = ["15"]#["13", "15"]          # <---

pNr, durchgang = 3, "3" 


folderEEG : str = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\rawEEG"
file_id = f"participant{pNr}_singleSpeaker"
pathVHDR  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vhdr"
pathVMRK  : str = folderEEG + f"\\participant{pNr}\\{file_id}.vmrk"


rawFull = mne.io.read_raw_brainvision( vhdr_fname = pathVHDR, ignore_marker_types = True, preload = True )

l_freq      = 1.0
h_freq      = 60.0
notch_freq  = 50.0
notch_width = 1.0

rawFull = rawFull.notch_filter( freqs = notch_freq, notch_widths = notch_width )
rawFull = rawFull.filter( l_freq = l_freq, h_freq = h_freq )

bad_channels = []               
for i in range(1, 64+1):
    bad_channels.append(str(i))

used_channels = copy.deepcopy(recordingElectrodes)
if( referenceElectrodes != None ):
    used_channels.extend(referenceElectrodes)
for ch in used_channels :      # <---    
    bad_channels.remove(ch)  

rawFull.drop_channels(bad_channels)


if( referenceElectrodes != None ):
    rawFull = mne.set_eeg_reference( rawFull, ref_channels = referenceElectrodes )[0]








zBusses = Ereignisse.get_zBusse( pathVMRK )

voltages_attentionTrue   = []
voltages_attentionFalse  = []

volt_att_nonATT = [[],[]]
for i in range( 2 ):

    duration_sec = int(60*2.5) #2.5 min

    start     : float   = float( zBusses[ i ] ) / float( rawFull.info["sfreq"] )
    end       : float   = float( start + duration_sec )
    rawBlock  : object  = rawFull.copy().crop(tmin = start, tmax = end)

    voltage, times = mne.io.Raw.get_data(
        rawBlock,
        picks         = recordingElectrodes, 
        return_times  = True, 
        units         = "V",
    )

    voltage = voltage[0]
    

    len_interval = 5000 #50   # 0.1 sec
    start = 1            # FIRSTMOST SAMPLE REMOVED (BECAUSE RAWBLOCK IS 15001 SAMPLES LONG)
    end   = start + len_interval
    
    while( end <= 75001 ): #len rawBlock
        voltage_interval = copy.deepcopy( voltage[start:end])
        volt_att_nonATT[i].append(voltage_interval)
        start = start + int(len_interval/2)  
        end   = start + len_interval

times = times[0:len_interval] #re-uses last value from loop

print(len(times))
print(len(volt_att_nonATT[0]))
print(len(volt_att_nonATT[1]))

avgVolt = [[],[]]
for a in range( 2 ):
    for j in range( len(times) ):

        voltagesForSample = []
        for intervalNr in range( len( volt_att_nonATT[a]) ):
            voltagesForSample.append( volt_att_nonATT[a][intervalNr][j] )

        meanVoltForSample = float(sum(voltagesForSample)) / float(len(voltagesForSample))
        avgVolt[a].append(meanVoltForSample)   # i.e. avgVolt[a][j] = meanVoltSample


print(len(avgVolt[0]))
print(avgVolt)

plt.plot( times, avgVolt[1] )
plt.xlim( 5.9, 6.0 )
plt.show()
inp = input("any ")
