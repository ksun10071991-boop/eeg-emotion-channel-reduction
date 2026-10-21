"""
channel_reduction.py
====================
Core logic for EEG channel reduction, used with the LibEER framework.

Idea: after LibEER loads and preprocesses the SEED features, we intercept
the data and keep only a selected subset of channels (by index) before
training proceeds. This keeps the reduced-channel results directly
comparable to the full-channel baseline (identical preprocessing/training).

The SEED dataset uses 62 channels in a fixed order (see docs/channel_map.md).
Emotion-relevant information concentrates in frontal and temporal regions,
so channel subsets are chosen accordingly.
"""

import numpy as np

# The 62 SEED channels, in order. Index in this list == channel index.
SEED_CHANNELS = [
    'FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ',
    'F2', 'F4', 'F6', 'F8', 'FT7', 'FC5', 'FC3', 'FC1', 'FCZ', 'FC2',
    'FC4', 'FC6', 'FT8', 'T7', 'C5', 'C3', 'C1', 'CZ', 'C2', 'C4',
    'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4', 'CP6',
    'TP8', 'P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8',
    'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ',
    'O2', 'CB2'
]

# Brain-region groups (SEED layout). Frontal/temporal carry most emotion info.
REGIONS = {
    'prefrontal': ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4'],
    'frontal':    ['F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'],
    'temporal':   ['FT7', 'T7', 'FT8', 'T8'],
    'central':    ['FC1', 'C3', 'CZ', 'FCZ', 'FC2', 'C4'],
    'parietal':   ['CP1', 'CP2', 'CPZ', 'PZ', 'P3', 'P4'],
    'occipital':  ['PO7', 'POZ', 'PO8', 'O1', 'OZ', 'O2', 'CB1', 'CB2'],
}


def names_to_indices(channel_names):
    """Convert a list of channel names to their SEED indices."""
    return [SEED_CHANNELS.index(ch) for ch in channel_names]


def uniform_indices(n):
    """Pick n channels evenly spaced across the 62 (baseline selection)."""
    step = max(1, 62 // n)
    return list(range(0, 62, step))[:n]


def cut_channels(obj, keep_idx):
    """
    Recursively walk the (ragged, nested) SEED data structure and slice the
    channel dimension wherever a 62-channel array is found.

    The SEED data is a nested list:
        data[subject][...][...][time, 62, bands]
    with variable-length segments (hence we must NOT np.asarray the whole
    thing at once). We descend through lists and only slice at the leaf
    arrays whose second-to-last axis is 62.
    """
    if isinstance(obj, list):
        return [cut_channels(x, keep_idx) for x in obj]
    arr = np.asarray(obj)
    if arr.ndim >= 2 and arr.shape[-2] == 62:
        return np.take(arr, keep_idx, axis=-2)
    return obj


# ---- Example channel subsets used in the experiments ----

# 2 channels, good placement: frontal + temporal
GOOD_2CH = names_to_indices(['FP1', 'T8'])          # indices 0, 31

# 2 channels, poor placement (control): occipital
POOR_2CH = names_to_indices(['O1', 'O2'])           # indices 58, 60

# Frontal-prioritized subsets (prefrontal + frontal region)
FRONTAL_PRIORITY = names_to_indices(
    REGIONS['prefrontal'] + REGIONS['frontal']
)


if __name__ == '__main__':
    print("SEED has", len(SEED_CHANNELS), "channels")
    print("Uniform 32:", uniform_indices(32))
    print("Good 2ch (FP1,T8):", GOOD_2CH)
    print("Poor 2ch (O1,O2):", POOR_2CH)
