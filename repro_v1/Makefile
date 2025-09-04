.PHONY: toy prep train eval baseline api

toy:
	python tools/harvest.py --toy
prep:
	python tools/preprocess.py
train:
	python tasks/train.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
eval:
	python tasks/eval.py --task all
baseline:
	python tasks/baseline_logreg.py --task all
api:
	uvicorn apps.api:app --host 0.0.0.0 --port 8000
