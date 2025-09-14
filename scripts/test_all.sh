#!/usr/bin/env bash
set -euo pipefail
pytest -q
flake8 .
