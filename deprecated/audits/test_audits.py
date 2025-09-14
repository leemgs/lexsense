# tests/test_audits.py
from __future__ import annotations
import os
import numpy as np
import pytest

from audits.drift_detection import population_stability_index
from audits.factuality_audit import FactualityAuditor, ClaimAudit
from audits.projection import pca_scalar_projection, mean_cosine_distance_projection

# ----------------------------
# PSI / Drift Detection Tests
# ----------------------------
def test_psi_zones_stable_alert_alarm():
    rng = np.random.default_rng(42)

    # 안정(stable): 동일 분포
    prev = rng.normal(0.0, 1.0, size=8000)
    curr_same = rng.normal(0.0, 1.0, size=8000)
    res_stable = population_stability_index(curr_same, prev, bins=12)
    assert res_stable.zone == "stable", f"expected stable, got {res_stable.zone}, PSI={res_stable.psi:.4f}"

    # 경고(alert): 작은 평균 이동
    curr_alert = rng.normal(0.18, 1.0, size=8000)  # 소폭 이동
    res_alert = population_stability_index(curr_alert, prev, bins=12)
    assert res_alert.zone in ("alert", "alarm"), f"expected alert-ish, got {res_alert.zone}, PSI={res_alert.psi:.4f}"

    # 알람(alarm): 큰 평균/분산 변화
    curr_alarm = rng.normal(0.6, 1.3, size=8000)
    res_alarm = population_stability_index(curr_alarm, prev, bins=12)
    assert res_alarm.zone == "alarm", f"expected alarm, got {res_alarm.zone}, PSI={res_alarm.psi:.4f}"


# -----------------------------------
# Factuality Audit Tests (with mocks)
# -----------------------------------
@pytest.fixture
def auditor_fast(monkeypatch):
    """
    빠른 테스트용: NLI 호출을 모킹하여 GPU/네트워크 없이 실행.
    """
    aud = FactualityAuditor(nli_model="facebook/bart-large-mnli")

    def mock_nli_supported(premise, hypothesis):
        # 증거가 주장을 지지하는 상황
        return {"entail": 0.92, "contradict": 0.03, "neutral": 0.05}

    def mock_nli_contradicted(premise, hypothesis):
        # 증거가 주장을 반박하는 상황
        return {"entail": 0.02, "contradict": 0.93, "neutral": 0.05}

    def mock_nli_uncertain(premise, hypothesis):
        # 애매한 상황
        return {"entail": 0.34, "contradict": 0.21, "neutral": 0.45}

    # monkeypatch 객체에 함수 저장해두고 테스트에서 교체 사용
    aud._mock_nli_supported = mock_nli_supported
    aud._mock_nli_contradicted = mock_nli_contradicted
    aud._mock_nli_uncertain = mock_nli_uncertain

    # 기본은 supported로 세팅
    monkeypatch.setattr(aud, "_nli_score", aud._mock_nli_supported)
    return aud

def test_factuality_supported(auditor_fast, monkeypatch):
    # 기본은 supported 모킹
    claims = [{"claim": "EU AI Act was adopted in 2024.",
               "evidence_span": "In 2024, the European Union adopted the AI Act."}]
    res = auditor_fast.audit(claims, low_conf_threshold=0.75)
    assert len(res) == 1
    r: ClaimAudit = res[0]
    assert r.verdict == "supported"
    assert r.confidence >= 0.75
    assert r.numeric_ok and r.date_ok and r.jurisdiction_ok

def test_factuality_contradicted(auditor_fast, monkeypatch):
    # 반박 상황으로 모킹 교체
    monkeypatch.setattr(auditor_fast, "_nli_score", auditor_fast._mock_nli_contradicted)
    claims = [{"claim": "The regulation reduces fines by 50%.",
               "evidence_span": "The regulation sets maximum fines up to 7% of global turnover."}]
    res = auditor_fast.audit(claims, low_conf_threshold=0.75)
    r = res[0]
    assert r.verdict == "contradicted"
    assert r.confidence >= 0.75

def test_factuality_uncertain_and_low_conf_queue(auditor_fast, monkeypatch):
    # 애매 + 저신뢰 큐 라우팅 (confidence 낮게 설정)
    monkeypatch.setattr(auditor_fast, "_nli_score", auditor_fast._mock_nli_uncertain)
    claims = [{"claim": "Transpare]()
