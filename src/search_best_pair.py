"""
search_best_pair.py
===================
Exhaustive search for the best 2-electrode pair for emotion recognition.

Among 12 emotion-relevant candidate electrodes (frontal + temporal), all 66
two-electrode combinations are evaluated. Each combination is run through the
full LibEER SVM pipeline (via the KEEP_CHANNELS env var and cut_channels),
and results are ranked.

Key finding: pairs that include a temporal electrode (T7/T8) consistently
outperform frontal-only pairs. Best pair: F8 + T7 (74.7%).
"""

import os
import itertools

# 12 candidate electrodes (frontal 8 + temporal 4) and their SEED indices
CANDIDATES = {
    'FP1': 0, 'FP2': 2, 'AF3': 3, 'AF4': 4,
    'F3': 7, 'F4': 11, 'F7': 5, 'F8': 13,
    'T7': 23, 'T8': 31, 'FT7': 14, 'FT8': 22,
}

DATASET_PATH = "/content/drive/MyDrive/SEED_data"
LIBEER = "/content/LibEER"


def run_pair(idx1, idx2):
    """Run the LibEER SVM pipeline keeping only two channels; return accuracy."""
    keep = f"{idx1},{idx2}"
    cmd = (
        f'cd {LIBEER} && KEEP_CHANNELS="{keep}" python LibEER/svm_train.py '
        f'-dataset seed_de_lds -dataset_path "{DATASET_PATH}" '
        f'-setting seed_sub_dependent_front_back_setting -device cpu '
        f'2>/dev/null | tail -1'
    )
    out = os.popen(cmd).read()
    try:
        return float(out.split("acc :")[1].split("/")[0].strip())
    except Exception:
        return -1.0


def main():
    names = list(CANDIDATES.keys())
    pairs = list(itertools.combinations(names, 2))  # 66 combinations
    results = []
    for i, (a, b) in enumerate(pairs, 1):
        acc = run_pair(CANDIDATES[a], CANDIDATES[b])
        results.append((a, b, acc))
        print(f"[{i}/{len(pairs)}] {a}+{b}: {acc:.4f}")

    results.sort(key=lambda r: r[2], reverse=True)
    print("\nTOP 10 two-electrode pairs:")
    for a, b, acc in results[:10]:
        print(f"  {a} + {b}: {acc:.4f}")


if __name__ == "__main__":
    main()
