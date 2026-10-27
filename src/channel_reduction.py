"""
channel_reduction.py
====================
Core logic for EEG channel reduction, used with the LibEER framework.

After LibEER loads and preprocesses SEED features, we slice the channel
dimension to keep only selected electrode indices before training. This keeps
reduced-channel results directly comparable to the full-channel baseline
(identical preprocessing / model / split).
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


def names_to_indices(channel_names):
    """Convert channel names to their SEED indices."""
    return [SEED_CHANNELS.index(ch) for ch in channel_names]


def uniform_indices(n):
    """Pick n channels evenly spaced across the 62."""
    step = max(1, 62 // n)
    return list(range(0, 62, step))[:n]


def cut_channels(obj, keep_idx):
    """
    Recursively walk the (ragged, nested) SEED data structure and slice the
    channel dimension wherever a 62-channel array is found.

    SEED data is nested lists with variable-length segments, so we must NOT
    np.asarray the whole thing at once — only slice at leaf arrays whose
    second-to-last axis is 62.
    """
    if isinstance(obj, list):
        return [cut_channels(x, keep_idx) for x in obj]
    arr = np.asarray(obj)
    if arr.ndim >= 2 and arr.shape[-2] == 62:
        return np.take(arr, keep_idx, axis=-2)
    return obj


# Notable subsets from the experiments
BEST_2CH = names_to_indices(['F8', 'T7'])    # optimal pair found: 74.7%
POOR_2CH = names_to_indices(['O1', 'O2'])    # occipital control: 61.6%
