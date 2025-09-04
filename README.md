# Automated AI Trend Sensing — Reproducibility Guide

본 문서는  **가장 빠르게 재현 가능한 절차(필수만)**를 정리한 가이드입니다.  

repro_v1 (full) + repro_v2 (expanded)

---

## 0) 준비

```bash
unzip ai_trend_sensing_repro_full.zip
cd ai_trend_sensing_repro_full

# 공통 권장 (완전 재현성)
export PYTHONHASHSEED=0
export TOKENIZERS_PARALLELISM=false
# 첫 실행 시 HF 모델이 받아지면 이후엔 오프로도 가능
# export TRANSFORMERS_OFFLINE=1
```

---

## 1) v1: 풀 파이프라인 (권장 기본 루트)

```bash
cd repro_v1
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 데이터 준비
python tools/harvest.py --toy
python tools/preprocess.py

# 학습/평가
python tasks/train.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
python tasks/eval.py --task all

# 베이스라인(아블레이션)
python tasks/baseline_logreg.py --task all

# 리포트 생성(선택)
python apps/report.py --input data/processed/test.jsonl --out reports/test_reports.jsonl --summarizer t5-small
```

### ✅ v1 산출물 (확인 체크)
- 모델/지표: `models/all_distilbert-base-uncased/test_metrics.json`  
- 전처리 산출물: `data/processed/{train,dev,test}.jsonl`  
- 리포트: `reports/test_reports.jsonl`  

---

## 2) v2: 확장 분석 (ECE, 드리프트, 설명가능성, HITL)

```bash
cd ../repro_v2
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 동일한 데이터 준비
python tools/harvest.py --toy
python tools/preprocess.py

# 학습/평가
python tasks/train_transformer.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
python tasks/eval.py --task all

# (1) 캘리브레이션/ECE
python tasks/calibration_ece.py --model_dir models/all_distilbert-base-uncased   --split data/processed/test.jsonl --plot figures/ece_curve.pdf

# (2) 컨셉 드리프트(시뮬레이션 플롯)
python tasks/continual.py --plot figures/concept_drift_sim.pdf

# (3) 증거-연결 설명가능성(근거 스팬)
python tasks/explainability.py --split data/processed/test.jsonl   --out reports/evidence_linked.jsonl

# (4) 휴먼-인-더-루프(저신뢰 케이스만 검토)
python tasks/human_loop.py --model_dir models/all_distilbert-base-uncased   --split data/processed/test.jsonl --threshold 0.75

# (5) 리포트 생성(요약)
python tasks/report_gen.py --input data/processed/test.jsonl   --out reports/test_reports.jsonl --summarizer t5-small
```

### ✅ v2 산출물 (확인 체크)
- `figures/ece_curve.pdf` (신뢰도 다이어그램)  
- `figures/concept_drift_sim.pdf` (드리프트 곡선)  
- `reports/evidence_linked.jsonl` (근거 스팬 포함 결과)  
- `reports/test_reports.jsonl` (요약 리포트)  

---

## 3) Makefile (바쁠 때 원클릭 실행)

각 폴더에서:

```bash
# v1
make toy prep train eval baseline

# v2
make toy prep train eval ece drift explain human report
```

---

## 4) API (옵션)

```bash
# v1
cd repro_v1 && source .venv/bin/activate
uvicorn apps.api:app --host 0.0.0.0 --port 8000
# 브라우저: http://localhost:8000/items?split=test&limit=5

# v2
cd repro_v2 && source .venv/bin/activate
uvicorn apps.api:app --host 0.0.0.0 --port 8000
```

---

## 5) Docker (옵션)

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

## ⚠️ 자주 막히는 포인트 (빠른 해결)

- **체크포인트 다운로드**: 첫 실행 때 Hugging Face 모델이 받아집니다.  
  방화벽/프록시 환경이면 수동 다운로드 후 `TRANSFORMERS_OFFLINE=1` 설정  
- **메모리 부족(OOM)**: `--batch`를 낮추고 `--max_seq_len`을 256–384로 조정  
- **경고 메시지**: `TOKENIZERS_PARALLELISM=false` 설정  
- **Windows 환경**: `source .venv/bin/activate` 대신 `.\.venv\Scripts\activate` 사용  
