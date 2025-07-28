import mne

from Elektroden import Elektroden

class Roh:

    @staticmethod
    def lade_fullRaw(pathVHDR : str) -> mne.io.Raw:
        """ Loads Header BVR file. """
        raw = mne.io.read_raw_brainvision(      
            vhdr_fname = pathVHDR,
            ignore_marker_types = True, 
            preload = True,
            verbose = True 
        ) 
        return raw


    @staticmethod
    def assign_unusedChannels_asBads(raw):
        picks = Elektroden.get_usedElectrodes()      # Channels to keep
        bads = raw.ch_names.copy()
        for ch in picks:
            bads.remove(ch)
        raw.info["bads"].extend(bads)   # All other channels assigned as bads
        return raw
    
    
    
#######################################################################################################################################################