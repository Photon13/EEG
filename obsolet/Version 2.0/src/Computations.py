import numpy as np

class Computations:

    @staticmethod
    def snr_spectrum(psd, noise_n_neighbor_freqs=1, noise_skip_neighbor_freqs=1):
        """Compute SNR spectrum from PSD spectrum using convolution.

        Parameters
        ----------
        psd : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
            Data object containing PSD values. Works with arrays as produced by
            MNE's PSD functions or channel/trial subsets.
        noise_n_neighbor_freqs : int
            Number of neighboring frequencies used to compute noise level.
            increment by one to add one frequency bin ON BOTH SIDES
        noise_skip_neighbor_freqs : int
            set this >=1 if you want to exclude the immediately neighboring
            frequency bins in noise level calculation

        Returns
        -------
        snr : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
            Array containing SNR for all epochs, channels, frequency bins.
            NaN for frequencies on the edges, that do not have enough neighbors on
            one side to calculate SNR.
        """
        # Construct a kernel that calculates the mean of the neighboring
        # frequencies
        averaging_kernel = np.concatenate(
            (
                np.ones(noise_n_neighbor_freqs),
                np.zeros(2 * noise_skip_neighbor_freqs + 1),
                np.ones(noise_n_neighbor_freqs),
            )
        )
        averaging_kernel /= averaging_kernel.sum()

        # Calculate the mean of the neighboring frequencies by convolving with the
        # averaging kernel.
        mean_noise = np.apply_along_axis(
            lambda psd_: np.convolve(psd_, averaging_kernel, mode="valid"), axis=-1, arr=psd
        )

        # The mean is not defined on the edges so we will pad it with nas. The
        # padding needs to be done for the last dimension only so we set it to
        # (0, 0) for the other ones.
        edge_width = noise_n_neighbor_freqs + noise_skip_neighbor_freqs
        pad_width = [(0, 0)] * (mean_noise.ndim - 1) + [(edge_width, edge_width)]
        mean_noise = np.pad(mean_noise, pad_width=pad_width, constant_values=np.nan)

        return psd / mean_noise




    @staticmethod
    def snrSpektrumNEU(psd, n_includePerSide=1, n_skipPerSide=1):
        """ SNR = Signal/Noise
            SNR(fx) = Signal(fx)/Noise( fx )
            Noise( fx ) ist die Konvolution einer Wichtung mit den PSD-Werten der Nachbarfrequenzen
            Die Wichtung ist abh. v. Anzahl an Nachbar-Frequenzen, die in Noise-Berechnung eingegangen sind.
            Die *unmittelbaren* Nachbar-Frequenzen der Signal-Frequenz werden ignoriert. 
            
            Bsp.:   fx-2  fx-1  fx  fx+1  fx+2 
                    fx = Signal-Frequenz
                    n_skipPerSide = 1
                    n_includePerSide = 1

            => In die Noise-Bestimmung einbezogene Frequenzen 
            sind fx-2 und fx+2, 
            aber nicht fx-1, fx+1 (skipped),
            und nicht fx (Signal)"""

        n_includeGes = n_includePerSide * 2                                 # Anzahl inkludierter Frequenzen (d.h. Summe beider Seiten)
        n_includeGes = float(n_includeGes)
        wichtung     = 1.0 / n_includeGes                                   # Wichtungs-Parameter

        averaging_kernel = []                                               # Liste Wichtungs-Werte (Wichtungs-Parameter oder 0) für betrachteten Frequenz-Bereich
                                                                            # Betrachteter Freq-Bereich: Signal und dessen Nachbarn (included & skipped)
        averaging_kernel.extend( [wichtung] * n_includePerSide )
        averaging_kernel.extend( [0.0] * n_skipPerSide )
        averaging_kernel.extend( [0.0] * 1 )
        averaging_kernel.extend( [0.0] * n_skipPerSide )
        averaging_kernel.extend( [wichtung] * n_includePerSide)

        averaging_kernel = np.array(averaging_kernel)                       # Bsp. [ 0.5  0.5  0.0  0.0  0.0  0.5  0.5 ]
        ##
        mean_noise = np.convolve( psd[0], averaging_kernel, mode="valid" )  # Konvolution Psd-Werte mit Kernel (also Wichtungs-Array)

        neighboursPerSite = n_includePerSide + n_skipPerSide                # Anz. inkludierte und geskippte Nachbarn je Seite
        mean_noise = np.pad(                                                # Anhängen von NaN auf beiden Seiten des Arrays, jeweils so oft wie neighboursPerSite vorhanden sind
            mean_noise, 
            pad_width = (neighboursPerSite, neighboursPerSite),             # links, rechts
            constant_values = np.nan
        )
        snr = psd / mean_noise      # SNR = Signal/Noise
                                    # Jeder Entry != NaN wird durch zugehörigen Noise-Wert geteilt
        return snr






#psd = np.array([[0.,3.,2.,3.,77.3,5.0,6., 0.0]], np.float32)
#print( Computations.snrSpektrumNEU(psd, n_includePerSide=1, n_skipPerSide=1) )

