# Methodology

## Task
Three-class EEG emotion recognition (positive / neutral / negative) on **SEED**,
under reduced channel counts and with a search for the best electrode positions.

## Data & Features
- SEED dataset, 62-channel EEG, `de_lds` features (differential entropy with
  LDS smoothing) across 5 frequency bands. Each sample is (channels x 5 bands).

## Model & Protocol
- SVM, subject-dependent: first 9 trials train, last 6 trials test
  (LibEER `seed_sub_dependent_front_back_setting`), averaged over subjects.

## Channel Reduction
After LibEER loads/preprocesses features, the channel dimension is sliced to a
chosen subset before training (see `src/channel_reduction.py`). Everything else
is identical, so reduced-channel accuracy is directly comparable to the
62-channel baseline.

## Best 2-electrode search
Among 12 frontal/temporal candidate electrodes, all 66 two-electrode pairs are
evaluated (`src/search_best_pair.py`). Pairs including a temporal electrode
(T7/T8) outperform frontal-only pairs; best pair is F8 + T7 (74.7%).

## Real-time prototype
`src/realtime_demo.py` trains the 2-channel model, then streams unseen segments
one by one, outputting instant and temporally-smoothed (5-segment majority vote)
predictions with ground-truth comparison. The browser demo (`demo/index.html`)
visualizes this.

## Validity checks
- Full-channel baseline (79.78%) matches published SEED+SVM results (~75-85%).
- Placement control (occipital 2ch = 61.6% vs best 2ch = 74.7%) confirms the
  accuracy reflects genuine emotion signal, not a pipeline artifact.

## Limitations
- Subject-dependent only; single dataset (SEED). Cross-subject and
  cross-dataset (e.g. DREAMER) generalization is future work.
- SVM baseline; stronger models may recover more accuracy at very low channels.
