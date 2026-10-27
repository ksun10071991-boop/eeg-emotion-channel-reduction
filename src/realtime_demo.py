"""
realtime_demo.py
===============
Simulated real-time emotion recognition using 2 electrodes (F8 + T7).

A model is trained on part of a subject's data, then unseen segments are fed
in one by one to simulate a real-time stream. Each step outputs:
  - the instant prediction,
  - a temporally-smoothed prediction (majority vote over the last 5 segments),
and compares against the ground-truth label.

This is the software prototype of a wearable "read 2 electrodes -> output
emotion in real time" system. Replacing the simulated stream with a live EEG
device makes it truly real-time.

Requires `data` and `label` loaded via LibEER's get_data() (see method.md).
"""

import numpy as np
from collections import deque, Counter
from sklearn.svm import SVC
import time

# F8 = index 13, T7 = index 23  (the optimal 2-channel pair)
KEEP = [13, 23]
EMOTION = {0: "Negative", 1: "Neutral", 2: "Positive"}
WINDOW = 5


def extract(data, label, subj, keep_idx):
    """Flatten one subject's data into samples, keeping only keep_idx channels."""
    X, y = [], []
    for a in range(len(data[subj])):
        for b in range(len(data[subj][a])):
            block = np.array(data[subj][a][b])          # (time, 62, bands)
            if block.ndim != 3:
                continue
            picked = block[:, keep_idx, :].reshape(block.shape[0], -1)
            X.append(picked)
            y.append(np.argmax(np.array(label[subj][a][b]), axis=1))
    return np.vstack(X), np.concatenate(y)


def run(data, label, subj=0):
    X, y = extract(data, label, subj, KEEP)
    split = int(len(X) * 0.7)
    model = SVC().fit(X[:split], y[:split])
    X_stream, y_stream = X[split:], y[split:]

    print("Real-time emotion monitor (F8 + T7)\n")
    hist = deque(maxlen=WINDOW)
    correct = 0
    step = max(1, len(X_stream) // 25)
    for t, i in enumerate(range(0, len(X_stream), step), 1):
        raw = model.predict(X_stream[i].reshape(1, -1))[0]
        hist.append(raw)
        stable = Counter(hist).most_common(1)[0][0]
        truth = y_stream[i]
        if stable == truth:
            correct += 1
        print(f"[{t:02d}] instant: {EMOTION[raw]:8s} | "
              f"stable: {EMOTION[stable]:8s} | truth: {EMOTION[truth]:8s}")
        time.sleep(0.3)
    print(f"\nStable-prediction accuracy: {correct}/{t}")


if __name__ == "__main__":
    print("Load `data`, `label` via LibEER get_data(), then call run(data, label).")
