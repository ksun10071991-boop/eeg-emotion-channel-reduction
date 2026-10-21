# SEED 62-Channel Map

The SEED dataset uses a fixed 62-channel order (10-20 system). The index below
(0-based) is what `KEEP_CHANNELS` refers to.

| Idx | Ch | Idx | Ch | Idx | Ch | Idx | Ch |
|:--:|:--|:--:|:--|:--:|:--|:--:|:--|
| 0 | FP1 | 16 | FC3 | 32 | TP7 | 48 | P6 |
| 1 | FPZ | 17 | FC1 | 33 | CP5 | 49 | P8 |
| 2 | FP2 | 18 | FCZ | 34 | CP3 | 50 | PO7 |
| 3 | AF3 | 19 | FC2 | 35 | CP1 | 51 | PO5 |
| 4 | AF4 | 20 | FC4 | 36 | CPZ | 52 | PO3 |
| 5 | F7 | 21 | FC6 | 37 | CP2 | 53 | POZ |
| 6 | F5 | 22 | FT8 | 38 | CP4 | 54 | PO4 |
| 7 | F3 | 23 | T7 | 39 | CP6 | 55 | PO6 |
| 8 | F1 | 24 | C5 | 40 | TP8 | 56 | PO8 |
| 9 | FZ | 25 | C3 | 41 | P7 | 57 | CB1 |
| 10 | F2 | 26 | C1 | 42 | P5 | 58 | O1 |
| 11 | F4 | 27 | CZ | 43 | P3 | 59 | OZ |
| 12 | F6 | 28 | C2 | 44 | P1 | 60 | O2 |
| 13 | F8 | 29 | C4 | 45 | PZ | 61 | CB2 |
| 14 | FT7 | 30 | C6 | 46 | P2 |  |  |
| 15 | FC5 | 31 | T8 | 47 | P4 |  |  |

## Brain Regions & Emotion Relevance

| Region | Example channels | Emotion relevance |
|:--|:--|:--|
| Prefrontal (PF) | FP1, FP2, AF3, AF4 (idx 0–4) | **High** — frontal asymmetry encodes valence |
| Frontal (F) | F3, F4, F7, F8 (idx 5–13) | **High** |
| Temporal (T) | T7, T8, FT7, FT8 (idx 14, 22, 23, 31) | **High** — emotional processing |
| Central (C) | C3, Cz, C4 (idx 25, 27, 29) | Medium |
| Parietal (P) | P3, Pz, P4 | Low–Medium |
| Occipital (O) | O1, Oz, O2 (idx 58–61) | **Low** — mainly visual (used as control) |

## Consumer Device Reference

For context, common wearable EEG devices and their channels:

| Device | Channels | Positions |
|:--|:--:|:--|
| NeuroSky | 1 | single frontal |
| **Muse** | 4 | AF7, AF8 (forehead) + TP9, TP10 (behind ears) |
| Emotiv Insight | 5 | AF3, AF4, T7, T8, Pz |
| Emotiv EPOC X | 14 | full-head |

The frontal + temporal positions favored by this study align with the most
successful consumer devices (e.g. Muse), supporting the practicality of
low-channel emotion sensing.
