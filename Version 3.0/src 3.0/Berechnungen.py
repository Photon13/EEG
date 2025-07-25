import numpy as np
from typing import List
import mne
import numpy as np

from Konvertierung import Konvertierung

class Berechnungen:

    """
        P_fABC_normiert       = Berechnungen.berechnePower_P_fABC( [famA, famB, famC], freqs, psds_normiert )
        P_fLMR_normiert       = Berechnungen.bestimme_P_fLMR( freqComb, P_fABC_normiert )
        P_fTarget_normiert    = Berechnungen.bestimme_P_fTarget( P_fLMR_normiert, target )
        P_fNonTarget_normiert = Berechnungen.bestimme_P_fNonTarget( P_fLMR_normiert, target )

        print( "blockNr = "                               + COLORPURPLE + f"{blockNr}"               + COLOREND )
        print( "target = "                                + COLORGREEN  + f"{target}"                + COLOREND )
        print( f"P_fABC_normiert_BLOCK{blockNr} = "       + COLORCYAN   + f"{P_fABC_normiert}"       + COLOREND )
        print( f"P_fLMR_normiert_BLOCK{blockNr} = "       + COLORCYAN   + f"{P_fLMR_normiert}"       + COLOREND )
        print( f"P_fTarget_normiert_BLOCK{blockNr} = "    + COLORCYAN   + f"{P_fTarget_normiert}"    + COLOREND )
        print( f"P_fNonTarget_normiert_BLOCK{blockNr} = " + COLORCYAN   + f"{P_fNonTarget_normiert}" + COLOREND )
    
    """



    @staticmethod
    def berechnePower_P_fABC( fABC : List[float], freqs : np.ndarray, psds_normiert : np.ndarray, border : float ):
        """ Input: z.B. border = 0.25 -> P über alle f:   fX - 0.25 < f < fX + 0.25
            mit fX E fABC und fABC = [famA, famB, famC]"""
    
        P_fABC : List[float] = [0.0, 0.0, 0.0]
        for i in range( len(fABC) ):
            closeFreqs_Indices : List[float] = []

            for k in range( len(freqs) ):
                if( fABC[i]-border < freqs[k] < fABC[i]+border ):
                    closeFreqs_Indices.append(k)

            print(f"n included frequencies in border-range = {len(closeFreqs_Indices)}")

            sum : float = 0.0
            for cFI in closeFreqs_Indices:
                sum += psds_normiert[cFI]
            mean = sum / len(closeFreqs_Indices)
            P_fABC[i] = mean #! falsch
        return P_fABC


    @staticmethod
    def bestimme_P_fLMR( freqComb : str, P_fABC : np.ndarray ):
        return Konvertierung.get_P_fLMR( freqComb, P_fABC )
    

    @staticmethod
    def bestimme_P_fTarget( P_fLMR : List[float], target : str ):
        """ Output: Mittlere Power für alle Target-Streams. """
        arr = np.multiply(                                  # set non-target streams to 0.0
            P_fLMR,                                         # e.g. target="both"
            Konvertierung.bool_targetPerCond[ target ]      # arr = [P_fL, 0.0, P_fR]
        )
        sum = np.sum( arr )                     # sum of power values for all target streams
        n_values = np.count_nonzero( arr )      # number of target streams ( i.e. != 0.0 )
        P_fTarget = sum / n_values              # mean power of target streams
        return P_fTarget


    @staticmethod
    def bestimme_P_fNonTarget( P_fLMR : List[float], target : str ):
        """ Output: Mittlere Power für alle Non-Target-Streams. """
        arr = np.multiply(                                  # set target streams to 0.0
            P_fLMR,                                         # e.g. target="both"
            Konvertierung.bool_nonTargetPerCond[ target ]   # arr = [0.0, P_fM, 0.0]
        )
        sum = np.sum( arr )                     # sum of power values for all non-target streams
        n_values = np.count_nonzero( arr )      # number of non-target streams ( i.e. != 0.0 )
        P_fNonTarget = sum / n_values              # mean power of non-target streams
        return P_fNonTarget
    

    @staticmethod
    def get_psds( rawBlock, blockLength : int ):

        voltage= mne.io.Raw.get_data(
            rawBlock,
            picks="Cz", 
            reject_by_annotation=None, 
            return_times=False, 
            units='uV', # Microvolt
            tmin = 0.0,
            tmax = blockLength,
            verbose=True,
        )[0]

        psds, freqs = mne.time_frequency.psd_array_welch(
            voltage,
            sfreq = rawBlock.info["sfreq"],
            fmin=0,
            fmax=np.inf,
            n_fft=65536, # Power of two, die am nächsten an Länge Daten (rawBlock) liegt und > Länge Daten ist
            #n_overlap=0, #?
            #n_per_seg=5000, #10 sec  #niedrigere werte glätten PSD(f)
            n_per_seg=2000,
            #n_per_seg=500,
            n_jobs=None,
            average = None,
            window="hamming",
            remove_dc=False, #?
            output="power",
            verbose=None,
        )

        psds : np.ndarray = psds.mean(-1) # mittelt Daten der einzelnen Transformations-Segmente

        sum = 0
        for e in psds:
            sum += e
        mittlere_psd : float = float(sum) / float(len(psds)) # mittlere PDS 
        print(mittlere_psd)

        # Konvertiere zu dB:
        psds_dB : np.ndarray = 10*np.log10(psds)

        return psds, psds_dB, freqs

    


"""
#ALTERNATIVE:
spectrum = mne.io.Raw.compute_psd(
    rawFull, 
    "welch",
    picks = "Cz",
    reject_by_annotation = True,
    verbose=True,
)

psds, freqs = psd, freqs = spectrum.get_data(return_freqs=True)
Plots.plot_PSD(psds[0], freqs)
"""
