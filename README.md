# Automated AI Trend Sensing — Reproducibility (Final Bundle)

This bundle contains **two complementary codebases**:

- `repro_v1/ai_trend_sensing_repro/` — richer end-to-end implementation (harvest → preprocess → train/eval → baseline → report; Docker; API)
- `repro_v2/` — expanded modules (ECE calibration, concept drift, evidence-linked explainability, human-in-the-loop, reporting), plus streamlined recipes

## Quick Start

### Option A — Start with v1 (full pipeline)
```
cd repro_v1/ai_trend_sensing_repro
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tools/harvest.py --toy
python tools/preprocess.py
python tasks/train.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
python tasks/eval.py --task all
```

### Option B — Use v2 (extra analyses)
```
cd repro_v2
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tools/harvest.py --toy
python tools/preprocess.py
python tasks/train_transformer.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
python tasks/eval.py --task all
python tasks/calibration_ece.py --model_dir models/all_distilbert-base-uncased --split data/processed/test.jsonl --plot figures/ece_curve.pdf
python tasks/continual.py --plot figures/concept_drift_sim.pdf
python tasks/explainability.py --out reports/evidence_linked.jsonl
python tasks/human_loop.py --model_dir models/all_distilbert-base-uncased --split data/processed/test.jsonl --threshold 0.75
python tasks/report_gen.py --input data/processed/test.jsonl --out reports/test_reports.jsonl --summarizer t5-small
```

### Notes
- Both codebases fix seeds and expose config in `configs/config.yml`.
- After first HF model download, set `TRANSFORMERS_OFFLINE=1` for offline runs.
- For Docker usage, see `repro_v1/ai_trend_sensing_repro/docker/` and `repro_v2/docker/`.

Enjoy, and cite the paper if you use these artifacts.
