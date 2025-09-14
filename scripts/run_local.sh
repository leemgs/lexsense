#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start backend
uvicorn lexsense.api:app --host 0.0.0.0 --port 8000 &
BACK_PID=$!

# Start dashboard
export BACKEND_URL=http://localhost:8000
streamlit run lexsense/dashboard.py

# Cleanup on exit
kill ${BACK_PID} 2>/dev/null || true
