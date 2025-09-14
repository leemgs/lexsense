# audits/drift_detection.py
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Tuple
from sklearn.preprocessing import StandardScaler

@dataclass
class PSIResult:
    psi: float
    band_edges: np.ndarray
    p_hist: np.ndarray
    q_hist: np.ndarray
    zone: str  # "stable" | "alert" | "alarm"

def _histogram(a: np.ndarray, bins: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    hist, edges = np.histogram(a, bins=bins)
    # avoid zero-count -> apply small additive smoothing
    hist = hist.astype(float) + 1e-6
    hist /= hist.sum()
    return hist, edges

def population_stability_index(
    current: np.ndarray,
    previous: np.ndarray,
    bins: int = 10,
    standardize: bool = True,
    thresholds=(0.1, 0.2),
) -> PSIResult:
    """
    Compute PSI between current and previous distributions.
    Inputs can be 1-D scores (e.g., projection of embeddings),
    or flattened distances. For multi-dim embeddings, provide
    a scalar projection beforehand (e.g., first PCA comp).
    """
    current = np.asarray(current).ravel()
    previous = np.asarray(previous).ravel()
    if standardize:
        scaler = StandardScaler().fit(previous.reshape(-1, 1))
        current = scaler.transform(current.reshape(-1, 1)).ravel()
        previous = scaler.transform(previous.reshape(-1, 1)).ravel()

    q_hist, edges = _histogram(previous, bins=bins)
    p_hist, _ = np.histogram(current, bins=edges)
    p_hist = p_hist.astype(float) + 1e-6
    p_hist /= p_hist.sum()

    psi = float(np.sum((p_hist - q_hist) * np.log(p_hist / q_hist)))

    if psi < thresholds[0]:
        zone = "stable"
    elif psi < thresholds[1]:
        zone = "alert"
    else:
        zone = "alarm"

    return PSIResult(psi=psi, band_edges=edges, p_hist=p_hist, q_hist=q_hist, zone=zone)
