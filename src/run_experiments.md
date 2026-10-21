# Reproducing the Experiments

These experiments run on top of the [LibEER](https://github.com/XJTU-EEG/LibEER)
framework with the SEED dataset. Below is the full procedure.

## 1. Environment (Google Colab recommended)

```bash
git clone https://github.com/XJTU-EEG/LibEER.git
cd LibEER
pip install -r requirements.txt
pip install torch_geometric skorch braindecode==0.7
```

Minor compatibility fixes needed for recent Python/library versions:
- comment out `from symbol import trailer` in `data_utils/load_data.py`
  (the `symbol` module was removed in Python 3.10+)
- reorder the `val_label = np.argmax(...)` line in `svm_train.py` so it runs
  only when a validation set exists (handles the front-back split with no val set)

## 2. Data

Request the **SEED** dataset from BCMI Lab (SJTU). Use the
`ExtractedFeatures` folder (`de_lds` features). Place the `.mat` files and
`label.mat` so LibEER finds them under `<dataset_path>/ExtractedFeatures/`.

## 3. Inject channel reduction

In LibEER's `data_utils/load_data.py`, inside `get_data()`, just before the
final `return`, insert channel slicing controlled by an environment variable
(`KEEP_CHANNELS`). See `channel_reduction.py` for the `cut_channels` logic.

```python
import os, numpy as np
keep = os.environ.get('KEEP_CHANNELS', '')
if keep:
    keep_idx = [int(x) for x in keep.split(',')]
    all_data = cut_channels(all_data, keep_idx)   # from channel_reduction.py
    channels = len(keep_idx)
```

## 4. Run the sweep

Baseline (all 62 channels):

```bash
python svm_train.py -dataset seed_de_lds -dataset_path <PATH> \
  -setting seed_sub_dependent_front_back_setting -device cpu
```

Reduced channels — set `KEEP_CHANNELS` to the indices to keep. Examples:

```bash
# 32 channels (uniform)
KEEP_CHANNELS="0,2,4,6,...,60" python svm_train.py ... (same args)

# 2 channels, good placement (FP1 + T8)
KEEP_CHANNELS="0,31" python svm_train.py ...

# 2 channels, poor placement control (O1 + O2)
KEEP_CHANNELS="58,60" python svm_train.py ...
```

Read the final line `ALLRound Mean and Std of acc : <mean>/<std>` for the result.

## 5. Results

Collected in `../results/results.csv` and plotted in
`../figures/channel_accuracy_curve.png`.
