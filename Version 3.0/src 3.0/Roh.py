import mne

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
    def get_mapping():
        #     Position     |  Elektrode    |  BVR Channel
        #__________________|_______________|_______________
        #    leftEar(A1)   |    13 grün    |      C3
        #    vertex(Cz)    |    14 grün    |      Cz
        #    rightEar(A2)  |    15 grün    |      C4


        mapping : dict = {              # old Channel name : new Channel name
            "13"  :  "A1",
            "14"  :  "Cz",
            "15"  :  "A2",
        }
 
        return mapping

    @staticmethod
    def renameChannels(raw):

        mapping = Roh.get_mapping()
        raw.rename_channels( 
            mapping = mapping,
            verbose = True
        )
        return raw
    

    @staticmethod
    def assign_unusedChannels_asBads(raw):
        picks = ["Cz", "A1", "A2"]      # Channels to keep
        bads = raw.ch_names.copy()
        for ch in picks:
            bads.remove(ch)
        raw.info["bads"].extend(bads)   # All other channels assigned as bads
        return raw
    
    
    @staticmethod
    def changeReference_toAverageAuricles(raw):
        refDict : dict = {
            "Cz" : ["A1","A2"]
        }
        raw = mne.set_eeg_reference(    # Replace Channel Cz with Cz - mean(A1,A2)
            raw, 
            ref_channels = refDict,
            #ref_channels = ["A1"],
            verbose = True 
        )[0]
        return raw
    
#######################################################################################################################################################