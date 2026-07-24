# LexSense (Starter) — Reproducible Framework & GovSense-1k Benchmark

This repository is a **reproducible starter kit** for the LexSense framework described in the paper.
It includes:

- **Synthetic benchmark**: `GovSense-1k` (1,200 items; Governance/Contract/Lawsuit/Asset = 400/300/250/250) with multilingual coverage.
- **Baselines**: TF‑IDF + Logistic Regression for 4‑way classification.
- **Utilities**: Concept‑drift (PSI) utility, factuality‑audit stubs, LLM reporter stub.
- **Dockerfile** & scripts for quick start.

> Paper reference: LexSense — Multilingual AI for Inclusive Access to Legal and Government Information. See the manuscript for task definition, dataset proportions, and evaluation outline.

## Quick Start

```bash
# 1) Create a virtualenv and install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) (Optional) Regenerate the synthetic GovSense-1k dataset
python scripts/generate_govsense_1k.py --out data/govsense_1k

# 3) Train a baseline
python -m lexsense.train_classifier --data_dir data/govsense_1k --out_dir data/govsense_1k/baseline_lr

# 4) Evaluate
python -m lexsense.evaluate --data_dir data/govsense_1k --model_dir data/govsense_1k/baseline_lr
```

## Dataset: GovSense‑1k (Synthetic for Reproducibility)

- **Total**: 1,200 items
- **Labels**: `governance` (400), `contract` (300), `lawsuit` (250), `asset` (250)
- **Languages**: primarily `en`, `ko`, `fr`, with a small stress subset in `es`, `ar`, `vi`
- **Fields**: `id`, `title`, `body`, `category`, `jurisdiction`, `language`, `timestamp`, `url`, `evidence_spans`

Data lives under `data/govsense_1k/`:
- `govsense_1k.jsonl` (full corpus)
- `train.jsonl`, `dev.jsonl`, `test.jsonl`
- `labels.csv` (label distribution)

> This synthetic set mirrors the proportions and task setup described in the paper to support **code‑path verification** end‑to‑end without external data access.

## Project Layout

```
src/lexsense/
  ingest/generator_govsense.py   # dataset generator
  taxonomy.py                    # label taxonomy & mapping
  preprocess.py                  # text cleaning & splitting
  train_classifier.py            # TF-IDF + Logistic Regression baseline
  evaluate.py                    # metrics and report
  drift.py                       # PSI for concept drift
  audit.py                       # factuality audit stubs
  reporter.py                    # LLM report generation stub
scripts/
  generate_govsense_1k.py
data/govsense_1k/
  govsense_1k.jsonl, train.jsonl, dev.jsonl, test.jsonl, labels.csv
```

## Docker

```bash
docker build -t lexsense:starter .
docker run --rm -it -v "$PWD":/app lexsense:starter   python -m lexsense.train_classifier --data_dir data/govsense_1k --out_dir data/govsense_1k/baseline_lr
```

## License

Apache-2.0 — see `LICENSE.md`.
