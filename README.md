
# LexSense — Reproducibility Guide
<img src="./lexsense.png" alt="LexSense" width="200" height="200">


This document summarizes the **minimal essential steps** for the fastest possible reproduction.

`repro_v1 (full)` + `repro_v2 (expanded)`

The rapid growth of generative AI has intensified demands for governance and compliance. Existing monitoring tools---manual reports, keyword alerts, and static trackers---cannot keep pace with dynamic, global regulatory changes. We introduce LexSense, a unified framework combining (1) real-time change detection, (2) semantic data acquisition, and (3) LLM-driven reporting. A novel taxonomy enables fine-grained classification of governance documents, contracts, lawsuits, and AI asset releases across jurisdictions and languages. Experiments on EU, U.S., and Korean datasets achieve 91\% accuracy, 82\% less analyst effort, and 70% faster reporting than manual baselines. Cross-lingual tests and ablations confirm robustness. We release full code, datasets, and Dockerized pipelines for reproducibility. Beyond technical gains, LexSense integrates fairness-aware tuning, bias audits, and privacy-preserving monitoring. Together, these contributions establish AI Governance Informatics as a new research direction, offering both a deployable compliance infrastructure and a conceptual foundation for scalable, transparent, and responsible AI governance.



---

## 0) Preparation

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

## 1) v1: Full Pipeline (Recommended Default Route)

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

## 2) v2: Extended Analysis (ECE, Drift, Explainability, HITL)

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

## 3) Makefile (One-click Execution When Busy)

From within each folder:

```bash
# v1
make toy prep train eval baseline

# v2
make toy prep train eval ece drift explain human report
```

---

## 4) API (Optional)

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

## 5) Docker (Optional)

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
