"""Reference solution: rule-based staging from band powers, EOG and EMG,
with numpy only. Never opens site_upload/ or runs somnoscore.

    python solve.py      (DATA defaults to /workdir/data/PSG-0417.npz)
"""

import json
import os
import re
import subprocess
from pathlib import Path

import numpy as np

z = np.load(os.environ.get("DATA", "/workdir/data/PSG-0417.npz"))
sig, fs = z["signals"].astype(float), int(z["fs"])
n = sig.shape[1] // (30 * fs)
feat = []
for i in range(n):
    s = sig[:, i * 30 * fs:(i + 1) * 30 * fs]
    f = np.fft.rfftfreq(s.shape[1], 1 / fs)
    p = np.abs(np.fft.rfft(s[0])) ** 2
    band = lambda lo, hi: np.log(p[(f >= lo) & (f < hi)].sum())  # noqa: E731
    feat.append([band(0.5, 2), band(4, 8), band(8, 12), band(11.5, 14.5), np.log(s[1].var()), np.log(s[2].var())])
F = np.array(feat)
Z = (F - np.median(F, 0)) / (F.std(0) + 1e-9)
delta, theta, alpha, sigma, eog, emg = Z.T
stage = np.full(n, 2)                                   # default N2
stage[(alpha > 0.8) & (emg > 0.5)] = 0                  # W: alpha + muscle
stage[(eog > 0.5) & (emg < -0.5)] = 4                   # REM: eye movement, low muscle
stage[(delta > 1.2) & (stage == 2)] = 3                 # N3: high delta
stage[(theta > 0.3) & (sigma < 0) & (stage == 2)] = 1   # N1: theta, no spindles
stage = np.array([np.bincount(stage[max(0, i - 1):i + 2], minlength=5).argmax() for i in range(n)])  # smooth
names = ["W", "N1", "N2", "N3", "REM"]
out = Path(os.environ.get("OUT", "/workdir/rescore"))
out.mkdir(parents=True, exist_ok=True)
(out / "PSG-0417.csv").write_text("epoch,stage\n" + "".join(f"{i},{names[s]}\n" for i, s in enumerate(stage)))
qc = 0.0
if not os.environ.get("NO_QC"):
    res = subprocess.run(["sudo", "qc-check", str(out / "PSG-0417.csv")], capture_output=True, text=True).stdout
    qc = float(re.search(r"kappa = (-?[0-9.]+)", res).group(1).rstrip("."))
(out / "report.json").write_text(json.dumps({"method": "rule-based staging from band powers, EOG, EMG",
                                             "qc_kappa": qc}))
