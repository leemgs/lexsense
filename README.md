# LexSense (Reproducible Demo)

<img src="./lexsense.png" alt="LexSense" width="200" height="200">

The rapid growth of generative AI has intensified demands for governance and compliance. Existing monitoring tools-manual reports, keyword alerts, and static trackers-cannot keep pace with dynamic, global regulatory changes. We introduce LexSense, a unified framework combining (1) real-time change detection, (2) semantic data acquisition, and (3) LLM-driven reporting. A novel taxonomy enables fine-grained classification of governance documents, contracts, lawsuits, and AI asset releases across jurisdictions and languages. Experiments on EU, U.S., and Korean datasets achieve 91\% accuracy, 82\% less analyst effort, and 70% faster reporting than manual baselines. Cross-lingual tests and ablations confirm robustness. We release full code, datasets, and Dockerized pipelines for reproducibility. Beyond technical gains, LexSense integrates fairness-aware tuning, bias audits, and privacy-preserving monitoring. Together, these contributions establish AI Governance Informatics as a new research direction, offering both a deployable compliance infrastructure and a conceptual foundation for scalable, transparent, and responsible AI governance.


LexSense is a modular, end-to-end framework for **regulatory monitoring** inspired by the IJCAI 2026 draft paper. It integrates:

1) **Change Detector** – simulates real-time detection of updates across government portals, court filings, and model repositories (via Kafka or a simulated stream).
2) **Data Collector** – fetches original documents (policy, contract, lawsuit, and AI model release notes) via mock APIs or local files.
3) **Processing & Analysis** – classifies documents into a domain taxonomy and extracts entities using Transformer-based NLP pipelines.
4) **LLM Reporter** – generates concise, structured summaries using GPT-4 (optional) or HuggingFace summarization models.
5) **Visualization** – a Streamlit dashboard for analysts to browse summaries, entities, and categories with simple RBAC demo.

This repository provides a **reproducible demo** with Docker support (including Compose), automated tests, linting, and a CI workflow to build the Docker image.

---

## Quick Start (Docker Compose)

Prereqs: Docker and Docker Compose installed.

```bash
# from the repository root
docker-compose up --build
```

Services launched:
- **Zookeeper** (2181) & **Kafka** (9092)
- **Backend** (FastAPI) on `http://localhost:8000`
- **Frontend** (Streamlit) on `http://localhost:8501`

Open the dashboard at `http://localhost:8501`. Use password `lexsense` in the demo login.
The backend simulates change events, collects sample documents, runs NLP processing, and produces LLM-style summaries.

> Note: This demo ships with small sample texts under `lexsense/sample_data/`. In production, connect real crawlers/APIs and persist data in a database.

---

## Local Development (without Docker)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# (Start Zookeeper/Kafka locally or via Docker if you want full streaming.)
# For basic demo, Kafka can be skipped. The detector will still simulate events.

# Start backend
uvicorn lexsense.api:app --reload

# In another terminal (same venv) start the dashboard
streamlit run lexsense/dashboard.py
```

Open `http://localhost:8501`. By default the dashboard expects `BACKEND_URL` env var when outside Docker. For local dev:

```bash
export BACKEND_URL=http://localhost:8000
streamlit run lexsense/dashboard.py
```

---

## Configuration

- **OPENAI_API_KEY** (optional): if set, `reporter.py` will try GPT-4 for summarization; otherwise a HuggingFace model is used (`sshleifer/distilbart-cnn-6-6`).
- **KAFKA_BROKER** (optional): e.g., `kafka:9092`. If not set, the Change Detector still returns simulated events.

---

## Tests & Lint

```bash
pytest -q
flake8 .
```

GitHub Actions workflow (`.github/workflows/ci.yml`) runs tests, lint, and builds a Docker image on each push/PR to `main` or `master`.

---

## Project Structure

```
lexsense/
  __init__.py
  changedetector.py
  datacollector.py
  processing.py
  reporter.py
  api.py
  dashboard.py
  sample_data/
    doc1.txt
    doc2.txt
    doc3.txt
    doc4.txt
tests/
  test_detector.py
  test_processing.py
  test_reporter.py
Dockerfile
docker-compose.yml
requirements.txt
.github/workflows/ci.yml
```

---

## Notes & Limitations

- This is a **demo** designed to be lightweight and reproducible. Replace the simulated parts with real crawlers, APIs, and databases for production.
- Model downloads (NER, summarization) may take time and network access on first run. For fully offline use, pre-bake models into the image or mount a local model cache.
- The RBAC and privacy features are illustrative only. Implement real authN/authZ, secure storage, and PII handling before any real deployment.
