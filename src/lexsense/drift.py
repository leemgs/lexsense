import numpy as np

def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10):
    # Population Stability Index on 1D feature
    # expected, actual: 1D arrays
    e_hist, edges = np.histogram(expected, bins=bins)
    a_hist, _ = np.histogram(actual, bins=edges)
    e_ratio = (e_hist + 1e-12) / max(e_hist.sum(), 1e-12)
    a_ratio = (a_hist + 1e-12) / max(a_hist.sum(), 1e-12)
    diff = (e_ratio - a_ratio) * np.log(e_ratio / a_ratio)
    return diff.sum(), edges.tolist()
