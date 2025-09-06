# audits/projection.py
from __future__ import annotations
import numpy as np
from typing import Optional
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

def pca_scalar_projection(
    embeddings: np.ndarray,
    n_components: int = 1,
    whiten: bool = False,
    random_state: int = 0,
) -> np.ndarray:
    """
    임베딩(문서/문장) 행렬을 PCA로 투영하여 1차 성분 점수를 스칼라로 반환.
    - embeddings: shape (N, D)
    - return: shape (N,)
    """
    if embeddings.ndim != 2:
        raise ValueError("embeddings must be 2-D array (N, D)")
    if embeddings.shape[0] < 2:
        raise ValueError("need at least 2 samples for PCA")

    pca = PCA(n_components=max(1, n_components), whiten=whiten, random_state=random_state)
    comps = pca.fit_transform(embeddings)  # (N, n_components)
    # 1차 성분만 사용 (스칼라)
    return comps[:, 0].astype(float)

def mean_cosine_distance_projection(
    embeddings: np.ndarray,
    ref_vector: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    임베딩을 기준 벡터(평균 임베딩 기본값)와의 코사인 거리로 변환한 스칼라 점수.
    - embeddings: (N, D)
    - ref_vector: (D,) or None -> None이면 평균 임베딩 사용
    - return: (N,)
    """
    if embeddings.ndim != 2:
        raise ValueError("embeddings must be 2-D array (N, D)")

    if ref_vector is None:
        ref_vector = embeddings.mean(axis=0)

    X = normalize(embeddings, axis=1)
    r = normalize(ref_vector.reshape(1, -1), axis=1)[0]
    # 코사인 유사도 → 거리 = 1 - sim
    sims = (X @ r)
    dists = 1.0 - sims
    return dists.astype(float)
