# Reproducibility Guide – LexSense

This guide explains how to reproduce the LexSense demo as described in the paper.

## 1) Requirements
- Hardware: x86-64 CPU (4+ cores), 16+ GB RAM; NVIDIA GPU (CUDA 11.7+) recommended
- Software: Python 3.10+, Docker + Docker Compose, Git

## 2) Quick Start (Docker) – Recommended
```bash
docker-compose up --build
```
- Backend (FastAPI): http://localhost:8000
- Dashboard (Streamlit): http://localhost:8501  (demo password: `lexsense`)

## 3) Local (no Docker)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn lexsense.api:app --reload
export BACKEND_URL=http://localhost:8000
streamlit run lexsense/dashboard.py
```

## 4) Data
Sample documents live in `lexsense/sample_data/`:
- `doc1.txt` (EU AI Act), `doc2.txt` (contract clause), `doc3.txt` (lawsuit), `doc4.txt` (AI model release).

## 5) Pipeline
1. Change Detector → simulated change events (Kafka optional)
2. Data Collector → loads sample docs
3. Processing & Analysis → classification + entity extraction (HF NER or regex fallback)
4. Reporter → summarization (GPT‑4 if `OPENAI_API_KEY` is set, else HF DistilBART)
5. Dashboard → table, chart, RBAC demo (guest vs analyst)

## 6) Tests & Lint
```bash
pytest -q
flake8 .
```

## 7) Scripts
- `scripts/run_docker.sh` → build & run all services
- `scripts/run_local.sh` → start backend & dashboard locally
- `scripts/test_all.sh` → run tests and flake8

## 8) Notes
- First run may download models.
- Kafka is included via Compose; pipeline also works in simulated mode.
- RBAC/auth is a minimal demo; do not use as-is for production.
