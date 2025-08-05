# self-made psd creating function (using psd_array_welch()) does not give the same output as compute_psd()
# -> different psd-values ca. -15 VS ca. -137 (whatever the units are (?))

# after putting n_fft, n_per_seg and n_overlap into psd_array_welch, multiple graphs are shown in plot, not a single one!


import mne
import numpy as np
import matplotlib
matplotlib.use('TkAgg') #choose TkAgg backend to display graphics
import matplotlib.pyplot as plt
plt.ion() #enables interactive mode for pyplot
from pathlib import Path
import os
from meegkit import dss
from collections import defaultdict

import json



participantNr = 2
durchgang = 2

picks = ['20', '25', '27']
reference = "average"




blockLength  = 30
n_blocks     = 72
famA = 35.9
famB = 39.7
famC = 43.2


pathBlockDict = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\BrainVision Recorder\\Version 3.0\\data\\blockDict\\participant2_blockDict.txt"

with open( pathBlockDict, "r" ) as f:
    block_dict = json.load(f)

import mne
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()
from pathlib import Path
import os
from meegkit import dss

#default_path = Path('C:/Users/pppar/Downloads')
default_path = "d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files"
#eeg_path = default_path / 'participant2_mainExp2.eeg'
eeg_path = default_path + f"\\participant2\\participant2_mainExp2.eeg"
#header_path = default_path / 'participant2_mainExp2.vhdr'
header_path = default_path + f"\\participant2\\participant2_mainExp2.vhdr"
#marker_path = default_path / 'participant2_mainExp2.vmrk'
marker_path = default_path + f"\\participant2\\participant2_mainExp2.vmrk"

eeg_raw = mne.io.read_raw_brainvision(header_path, preload=True)
to_drop = [str(ch) for ch in np.arange(32, 65)]
eeg_raw.drop_channels(to_drop)
#eeg_raw.plot()
data = mne.io.RawArray(data=eeg_raw.get_data(), info=eeg_raw.info)
eeg_notch, iterations = dss.dss_line(eeg_raw.get_data().T, fline=50,
                                     sfreq=data.info["sfreq"],
                                     nfft=400)

eeg_raw._data = eeg_notch.T
hi_filter = 1
lo_filter = 60

eeg_filtered = eeg_raw.copy().filter(hi_filter, lo_filter)
#eeg_filtered.plot()

"""
ica = mne.preprocessing.ICA(n_components=0.999, method='fastica', random_state=99)
ica.fit(eeg_filtered)  # bad segments that were marked in the EEG signal will be excluded.
# b. investigate...:
ica.plot_sources(eeg_filtered)
# c. apply ICA to remove selected components: blinks, eye movements etc.
ica.apply(eeg_filtered)
"""
eeg_filtered.pick(picks)
eeg_filtered.set_eeg_reference('average')

from collections import defaultdict
grouped_blocks = defaultdict(list)
for block_name, info in block_dict.items():
    block_idx = int(block_name.replace("block", ""))
    key = f"{info['freqComb']}_{info['condition']}"
    grouped_blocks[key].append(block_idx)

# === Create blocks_array from EEG ===
events, event_id = mne.events_from_annotations(eeg_filtered)
block_start_events = events[events[:, 2] == 161]
block_samples = int(30 * eeg_filtered.info['sfreq'])  # 30s block
epochs = []
valid_onsets = []

for event in block_start_events:
    start = event[0]
    stop = start + block_samples
    if stop <= len(eeg_filtered.times):
        segment = eeg_filtered.get_data(start=start, stop=stop)
        epochs.append(segment)
        valid_onsets.append(start)

blocks_array = np.stack(epochs)  # shape: (n_blocks, n_channels, n_times)

# === Organize grouped data from blocks_array ===
grouped_data = {
    group: blocks_array[indices]
    for group, indices in grouped_blocks.items()
}

# === --- SELECT GROUP FOR PSD --- ===
target_freqs = [35.9, 39.7, 43.2]

block_keys = list(grouped_blocks.keys())
for i, group in enumerate(block_keys):
    target_group = block_keys[i]
    sfreq = eeg_filtered.info['sfreq']
    ch_names = eeg_filtered.info['ch_names']

    # === Concatenate blocks of selected group ===
    group_blocks = grouped_data[target_group]
    concatenated_data = np.concatenate(group_blocks, axis=1)

    # === Create Raw object from concatenated data ===
    from mne import create_info, io

    ch_types = ['eeg'] * len(ch_names)
    info = create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    raw_group = io.RawArray(concatenated_data, info)

    """
    # === Compute high-res Welch PSD ===
    psd = raw_group.compute_psd(
        method='welch',
        fmin=30, fmax=55,
        n_per_seg=2000,
        n_overlap=1000,
        verbose=True
    )

    # Convert to dB
    psds_db = 10 * np.log10(psd.get_data())  # shape: (n_channels, n_freqs)
    print(psds_db)
    freqs = psd.freqs
    """

    psds, freqs = mne.time_frequency.psd_array_welch(
        x         = raw_group.get_data(),
        sfreq     = raw_group.info["sfreq"],
        n_fft     = 65536,
        n_per_seg = 5000,
        n_overlap = 2500,
        average   = None
    )
    psds_db = 10 * np.log10(psds)


    # === Average PSD across channels ===
    avg_psd = psds_db.mean(axis=0)

    # === Plot ===
    plt.figure(figsize=(10, 5))
    plt.plot(freqs, avg_psd, label="Average PSD (across channels)")

    # Vertical lines
    for tf in target_freqs:
        plt.axvline(tf, color='red', linestyle='--', alpha=0.8, linewidth=1.2)

    plt.title(f"PSD of Concatenated Blocks ({target_group})")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power Spectral Density [dB]")
    plt.xlim(34, 45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.savefig(fname = f"d:\\Maik\\Studium\\Biologie Bachelor\\Bachelorarbeit\\amplitudeModulation\\EEG files\\plots\participant2\\PSD_concatBlocks_{target_group}_picks_{picks}_ref_{reference}")
    #plt.show()
    #inp = input("any ")


    