import numpy as np
from typing import List
import re

COLORRED    = '\33[31m'
COLOREND = '\033[0m'


class Ereignisse:

    @staticmethod
    def get_ereignisse(pathVMRK : str):
        """ Extrahiert aus dem VMRK File die Marker-Ereignisse
            und generiert einen 3-dimensionalen npArray der Form [ [tSampAbs 0 markerNr] [...] ]. """
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
            "zBus" : 161,
            "shiftLeft" : 32,
            #"shiftMiddle" : 2,         # not existent for participant0
            "shiftRight" : 34,
            "button" : 128
        }
        print(COLORRED + "S  2 currently not used!. Remember to enable it in plotMarkers_perTime()." + COLOREND)
        return events_tSampAbs, event_dict
    

    @staticmethod
    def get_zBusse( pathVMRK ):
        """  Output: Liste mit Zeitpunkten [samples] der zBus-Marker """
        events_tSampAbs, event_dict = Ereignisse.get_ereignisse(pathVMRK)

        zBusses : List[int] = []
        for i in range( len(events_tSampAbs) ):             
            if( events_tSampAbs[i][2] == 161 ):
                zBusses.append( events_tSampAbs[i][0] )
        return zBusses
    
