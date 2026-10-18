"""Synthetic overnight PSG. physio = the sleeper's true stage per 30 s epoch;
tech = the original lab's technician hypnogram (physio with realistic
disagreement). Signals are generated from physio."""
import numpy as np
FS, EP = 64, 30
STAGES = ["W", "N1", "N2", "N3", "REM"]

def hypnogram(rng, n=960):
    seq, t = [], 0
    while len(seq) < n:
        cyc = len(seq) // 180
        seq += [0] * rng.integers(2, 12) + [1] * rng.integers(2, 8) + [2] * rng.integers(20, 50)
        seq += [3] * max(0, rng.integers(10, 40) - 8 * cyc) + [2] * rng.integers(5, 20) + [4] * (rng.integers(5, 15) + 6 * cyc)
    return np.array(seq[:n])

def technician(rng, physio, err):
    tech = physio.copy()
    for i in range(len(tech)):
        if rng.random() < err:
            s = physio[i]
            tech[i] = {0: 1, 1: rng.choice([0, 2]), 2: rng.choice([1, 3]), 3: 2, 4: rng.choice([1, 2])}[s]
    return tech

def signals(rng, physio, overlap):
    n = len(physio) * EP * FS
    t = np.arange(EP * FS) / FS
    eeg, eog, emg = (np.zeros(n, np.float32) for _ in range(3))
    # per-stage feature means (alpha, theta, spindle, delta, eye, emg)
    P = {0: (8, 3, 0, 2, 40, 20), 1: (3, 6, 0.5, 3, 10, 12), 2: (1.5, 5, 6, 6, 3, 8),
         3: (1, 4, 3, 22, 2, 7), 4: (2, 6, 0, 3, 35, 2)}
    for i, s in enumerate(physio):
        a, th, sp, de, ey, em = (max(0.1, v * (1 + overlap * rng.normal())) for v in P[s])
        seg = (a * np.sin(2*np.pi*10*t + rng.uniform(0, 6)) + th * np.sin(2*np.pi*6*t + rng.uniform(0, 6))
               + de * np.sin(2*np.pi*1.2*t + rng.uniform(0, 6)) + rng.normal(0, 4, len(t)))
        if sp > 0.3:
            for c in rng.uniform(0, EP - 1, rng.poisson(sp / 2)):
                k = (t > c) & (t < c + 1)
                seg[k] += 12 * np.sin(2*np.pi*13*t[k])
        sl = slice(i * EP * FS, (i + 1) * EP * FS)
        eeg[sl] = seg
        eog[sl] = ey * (rng.random(len(t)) < 0.02).astype(float).cumsum() % 2 - ey / 2 + rng.normal(0, 3, len(t))
        emg[sl] = rng.normal(0, em, len(t))
    return np.vstack([eeg, eog, emg])
