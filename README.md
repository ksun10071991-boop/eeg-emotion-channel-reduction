# EEG Emotion Recognition under Channel Reduction 🧠

### 脑电情绪识别的通道精简研究

> How few EEG electrodes do we actually need to recognize emotions?
> Using the SEED dataset, this project shows that accuracy drops only **7 percentage points** (79.8% → 72.7%) when reducing from **62 channels to 2**, and that **electrode placement matters as much as channel count**.

---

## Overview | 项目简介

This project investigates **channel reduction** for EEG-based emotion recognition — a key question for building low-cost, wearable emotion-sensing devices (which typically have only 2–14 electrodes, unlike the 62-electrode research systems).

Built on top of the [LibEER](https://github.com/XJTU-EEG/LibEER) framework and the **SEED** dataset (three-class emotion: positive / neutral / negative), the study systematically reduces the number of EEG channels and measures how accuracy changes.

本项目研究脑电情绪识别中的**通道精简**问题——这对低成本可穿戴情绪识别设备至关重要（消费级设备通常只有 2–14 个电极，而研究级系统有 62 个）。

## Key Findings | 核心发现

![Channel vs Accuracy](figures/channel_accuracy_curve.png)

1. **Massive channel redundancy.** Reducing from 62 → 2 channels costs only **7.1%** accuracy (79.8% → 72.7%). Emotion-relevant information is highly concentrated.

2. **2 channels are enough for a usable system.** Even with just **2 electrodes**, accuracy stays at **72.7%** — well above the 33.3% random baseline.

3. **Electrode placement is critical.** Two well-placed channels (frontal + temporal) reach 72.7%, while two poorly-placed channels (occipital) drop to 61.6% — a **~11% difference** from placement alone.

> **Implication:** A practical wearable emotion-sensing device does not need a dense electrode cap. A small number of *correctly placed* frontal/temporal electrodes can retain most of the accuracy.

## Results | 实验结果

| EEG Channels | Accuracy | Note |
|:---:|:---:|:---|
| 62 (full) | 79.78% | Baseline |
| 32 | 78.82% | −0.96% |
| 16 | 76.89% | |
| 8 | 76.92% | |
| 4 | 74.75% | |
| 2 (frontal+temporal) | **72.73%** | Good placement |
| 2 (occipital) | 61.60% | Poor placement (control) |

- **Dataset:** SEED (SJTU Emotion EEG Dataset), 3-class, `de_lds` features
- **Model:** SVM
- **Protocol:** subject-dependent, first 9 trials train / last 6 trials test
- **Baseline validity:** 79.78% is consistent with published SEED+SVM results (~75–85%)

## Method | 方法

Channel reduction is implemented by intercepting the data pipeline in LibEER: after features are loaded, the channel dimension is sliced to keep only the selected electrode indices, then the standard LibEER training proceeds unchanged. This ensures reduced-channel results are **directly comparable** to the full-channel baseline (same preprocessing & training).

See [`docs/method.md`](docs/method.md) for details and [`src/`](src/) for the implementation.

## Repository Structure | 项目结构

```
eeg-emotion-channel-reduction/
├── README.md
├── figures/
│   └── channel_accuracy_curve.png    # Main result figure
├── results/
│   └── results.csv                   # Raw accuracy numbers
├── src/
│   ├── channel_reduction.py          # Core channel-slicing logic
│   └── run_experiments.md            # Commands to reproduce
└── docs/
    ├── method.md                     # Methodology details
    └── channel_map.md                # SEED 62-channel layout & brain regions
```

## Reproduce | 复现

See [`src/run_experiments.md`](src/run_experiments.md) for step-by-step commands (environment setup, data, and running the channel-reduction sweep).

## Acknowledgements | 致谢

- **LibEER** framework: https://github.com/XJTU-EEG/LibEER
- **SEED** dataset: BCMI Lab, Shanghai Jiao Tong University

## License & Scope

Research / portfolio project, for non-commercial academic use. SEED dataset usage follows its own license (academic, non-commercial).

---

*A personal research project exploring low-channel EEG emotion recognition for wearable applications by Yannan Sun.*
