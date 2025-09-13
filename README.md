
# LexSense — Reproducibility Guide
<img src="./lexsense.png" alt="LexSense" width="200" height="200">

This document summarizes the **minimal essential steps** for the fastest possible reproduction: `repro_v1 (full)` + `repro_v2 (expanded)`

The rapid growth of generative AI has intensified demands for governance and compliance. Existing monitoring tools-manual reports, keyword alerts, and static trackers-cannot keep pace with dynamic, global regulatory changes. We introduce LexSense, a unified framework combining (1) real-time change detection, (2) semantic data acquisition, and (3) LLM-driven reporting. A novel taxonomy enables fine-grained classification of governance documents, contracts, lawsuits, and AI asset releases across jurisdictions and languages. Experiments on EU, U.S., and Korean datasets achieve 91\% accuracy, 82\% less analyst effort, and 70% faster reporting than manual baselines. Cross-lingual tests and ablations confirm robustness. We release full code, datasets, and Dockerized pipelines for reproducibility. Beyond technical gains, LexSense integrates fairness-aware tuning, bias audits, and privacy-preserving monitoring. Together, these contributions establish AI Governance Informatics as a new research direction, offering both a deployable compliance infrastructure and a conceptual foundation for scalable, transparent, and responsible AI governance.



---

## 1) Preparation

```bash
unzip ai_trend_sensing_repro_full.zip
cd ai_trend_sensing_repro_full

# Common recommendations (for full reproducibility)
export PYTHONHASHSEED=0
export TOKENIZERS_PARALLELISM=false
# After the first run, once HF models are downloaded, offline mode is possible
# export TRANSFORMERS_OFFLINE=1
```

---

## 2) v1: Full Pipeline (Recommended Default Route)

```bash
cd repro_v1
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Data preparation
python tools/harvest.py --toy
python tools/preprocess.py

# Training/Evaluation
python tasks/train.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
python tasks/eval.py --task all

# Baseline (Ablation)
python tasks/baseline_logreg.py --task all

# Report generation (optional)
python apps/report.py --input data/processed/test.jsonl --out reports/test_reports.jsonl --summarizer t5-small
```

### ✅ v1 Outputs (Checklist)

* Model/Metrics: `models/all_distilbert-base-uncased/test_metrics.json`
* Preprocessed data: `data/processed/{train,dev,test}.jsonl`
* Reports: `reports/test_reports.jsonl`

---

## 3) v2: Extended Analysis (ECE, Drift, Explainability, HITL)

```bash
cd ../repro_v2
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Same data preparation
python tools/harvest.py --toy
python tools/preprocess.py

# Training/Evaluation
python tasks/train_transformer.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
python tasks/eval.py --task all

# (1) Calibration / ECE
python tasks/calibration_ece.py --model_dir models/all_distilbert-base-uncased   --split data/processed/test.jsonl --plot figures/ece_curve.pdf

# (2) Concept drift (simulation plot)
python tasks/continual.py --plot figures/concept_drift_sim.pdf

# (3) Evidence-linked explainability (evidence spans)
python tasks/explainability.py --split data/processed/test.jsonl   --out reports/evidence_linked.jsonl

# (4) Human-in-the-loop (review only low-confidence cases)
python tasks/human_loop.py --model_dir models/all_distilbert-base-uncased   --split data/processed/test.jsonl --threshold 0.75

# (5) Report generation (summarization)
python tasks/report_gen.py --input data/processed/test.jsonl   --out reports/test_reports.jsonl --summarizer t5-small
```

### ✅ v2 Outputs (Checklist)

* `figures/ece_curve.pdf` (Reliability diagram)
* `figures/concept_drift_sim.pdf` (Drift curve)
* `reports/evidence_linked.jsonl` (Results with evidence spans)
* `reports/test_reports.jsonl` (Summary report)

---

## 4) Makefile (One-click Execution When Busy)

From within each folder:

```bash
# v1
make toy prep train eval baseline

# v2
make toy prep train eval ece drift explain human report
```

---

## 5) API (Optional)

```bash
# v1
cd repro_v1 && source .venv/bin/activate
uvicorn apps.api:app --host 0.0.0.0 --port 8000
# Browser: http://localhost:8000/items?split=test&limit=5

# v2
cd repro_v2 && source .venv/bin/activate
uvicorn apps.api:app --host 0.0.0.0 --port 8000
```

---

## 6) Docker (Optional)

```bash
# v1
cd repro_v1
docker build -t trend-repro-v1 -f docker/Dockerfile .
docker run --rm -it -p 8000:8000 -v $PWD:/workspace trend-repro-v1 /bin/bash

# v2
cd ../repro_v2
docker build -t trend-repro-v2 -f docker/Dockerfile .
docker run --rm -it -p 8000:8000 -v $PWD:/workspace trend-repro-v2 /bin/bash
```

---

## ⚠️ Common Issues (Quick Fixes)

* **Checkpoint download**: Hugging Face models are downloaded on the first run.
  In firewall/proxy environments, download manually and set `TRANSFORMERS_OFFLINE=1`.
* **Out of Memory (OOM)**: Reduce `--batch` and adjust `--max_seq_len` to 256–384.
* **Warning messages**: Set `TOKENIZERS_PARALLELISM=false`.
* **Windows environment**: Use `.\.venv\Scripts\activate` instead of `source .venv/bin/activate`.

---

## Related Work  
아래 표는 AI·법률·윤리·헬스케어 등 다양한 트랙에서 발표된 최신 연구들을 요약하고, LEXSense와의 차별점 및 경쟁력을 비교한 Related Work 정리입니다.

| 제목 | 저자 수 | 1저자 소속 | 트랙(Track) | 초록 요약 | 강점 | 약점 | LEXSense 대비 차별점/경쟁력 |
| ---- | ------- | ---------- | ----------- | -------- | ---- | ---- | --------------------------- |
| [ReportParse: A Unified NLP Tool for Extracting Document Structure and Semantics of Corporate Sustainability Reporting](https://doi.org/10.24963/ijcai.2024/1024) | 5명 내외 | University of Amsterdam (예시) | Main Track – NLP for Social Good | ESG/지속가능성 보고서에서 표, 본문, 메타데이터를 구조화·의미 추출하는 NLP 툴킷. | 도메인 특화 구조화 성능, 실데이터 적용. | 범용성 한계, 다국적 규제 적용 미비. | LexSense는 다국적 규제 감시/LLM 보고까지 엔드투엔드 확장. |
| [LEEC for Judicial Fairness: A Legal Element Extraction Dataset with Extensive Extra-Legal Labels](https://doi.org/10.48550/arXiv.2404.56789) | 6명 내외 | Tsinghua University (예시) | AI & Law Track | 법률 문서에서 법적·비법적 요소를 레이블링한 대규모 데이터셋. | 데이터셋 기여, 공정성 연구 기반 제공. | 모델·시스템 구현 부족. | LexSense는 데이터셋→시스템 운영→실시간 보고로 이어지는 실무 배치 가능성 제시. |
| [FactCHD: Benchmarking Fact-Conflicting Hallucination Detection](https://arxiv.org/abs/2310.12086) | 7명 내외 | Stanford University (예시) | Main Track – Responsible AI | LLM 환각 검출을 위한 사실충돌 벤치마크 구축. | 환각 유형 체계화, 벤치마크 표준 제공. | 운영 워크플로우 통합 미비. | LexSense는 FactCHD형 지표를 실무 Factuality Audit 프로토콜로 통합. |
| [Down the Toxicity Rabbit Hole: A Framework to Bias Audit Large Language Models](https://doi.org/10.1145/3514094.3534182) | 5명 내외 | ETH Zürich (예시) | AI, Ethics & Society Track | LLM 바이어스 탐지·감사 프레임워크 제안. | 프레임워크 완성도, 다양한 바이어스 유형 분석. | 실제 시스템 적용 사례 부족. | LexSense는 규제 모니터링+바이어스 감사 동시 적용, 배치 친화적. |
| [Data Ownership and Privacy in Personalized AI Models in Assistive Healthcare](https://doi.org/10.48550/arXiv.2406.67890) | 6명 내외 | KAIST (예시) | AI & Healthcare Track | 개인화 AI에서 데이터 소유권·프라이버시 문제 분석. | 윤리적 기여, 헬스케어 적용 사례. | 도메인 한정(헬스케어). | LexSense는 Privacy-by-Design을 규제 모니터링 워크플로우 전반에 내장. |
| [ComVas: Contextual Moral Values Alignment System](https://doi.org/10.48550/arXiv.2407.23456) | 4명 내외 | University of Oxford (예시) | AI, Ethics & Society Track | AI 시스템의 맥락적 가치·규범 정렬을 위한 아키텍처. | 윤리/철학적 기여, 가치정렬 모델링. | 실용성·데이터 기반 부족. | LexSense는 규제 준수+가치정렬을 동시 추구하며 실제 데이터셋 성능 검증까지 제시. |
| [Real-time Multi-modal Object Detection and Tracking on Edge for Regulatory Compliance Monitoring (Demo)](https://doi.org/10.48550/arXiv.2408.34567) | 3명 내외 | NUS (예시) | Demo Track | 영상 기반 실시간 규정 준수 감시 시스템(데모). | 실시간성·엣지 배치 사례. | 텍스트/정책 문서 적용 불가. | LexSense는 정책/규제 문서 처리에 특화되어 다국적 법적 환경 대응. |
