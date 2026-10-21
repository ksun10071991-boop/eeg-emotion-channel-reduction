# Methodology

## Task

Three-class EEG emotion recognition (positive / neutral / negative) on the
**SEED** dataset, under progressively reduced channel counts.

## Data & Features

- **Dataset:** SEED (SJTU Emotion EEG Dataset), 62-channel EEG, 15 subjects,
  3 sessions each, 15 film-clip trials per session.
- **Features:** `de_lds` (differential entropy with linear dynamic system
  smoothing) across 5 frequency bands — the standard, well-performing SEED
  feature. Each sample is `(62 channels × 5 bands)`.

## Model & Protocol

- **Model:** Support Vector Machine (SVM).
- **Protocol:** subject-dependent. For each subject, the first 9 trials are
  used for training and the last 6 for testing (LibEER's
  `seed_sub_dependent_front_back_setting`). Accuracy is averaged across
  subjects.

## Channel Reduction

The core manipulation is reducing the number of EEG channels while keeping
everything else fixed:

1. LibEER loads and preprocesses the SEED features as usual.
2. **Before training**, the channel dimension of the feature tensor is sliced
   to keep only a chosen subset of electrode indices (`cut_channels`).
3. The standard LibEER training then runs on the reduced data.

Because only the channel dimension changes, reduced-channel accuracies are
**directly comparable** to the 62-channel baseline — the preprocessing,
features, model, and train/test split are all identical.

## Channel Selection Strategies

- **Uniform:** evenly spaced indices across the 62 channels (e.g. every 2nd
  channel for 32). An unbiased baseline selection.
- **Placement contrast (2 channels):**
  - *Good:* FP1 (prefrontal) + T8 (temporal) — regions known to carry
    emotion-relevant information.
  - *Poor (control):* O1 + O2 (occipital) — a region less associated with
    emotional processing.

The good-vs-poor contrast isolates the effect of **electrode placement**
independent of channel count.

## Validity Checks

- The full-channel baseline (**79.78%**) matches published SEED + SVM results
  (~75–85%), indicating the pipeline is sound.
- The placement control (poor 2ch = 61.6% vs good 2ch = 72.7%) confirms the
  accuracy reflects genuine emotion-related signal, not a pipeline artifact:
  a leakage/bug would inflate *both* equally.

## Limitations

- Subject-dependent only (no cross-subject generalization tested here).
- Single dataset (SEED); cross-dataset generalization (e.g. DREAMER) is future
  work.
- SVM baseline; stronger models (DGCNN, RGNN) may recover more accuracy at
  very low channel counts.
