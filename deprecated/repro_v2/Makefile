.PHONY: toy prep train eval baseline ece drift explain human report api

toy:
	python tools/harvest.py --toy
prep:
	python tools/preprocess.py
train:
	python tasks/train_transformer.py --task all --epochs 5 --batch 16 --lr 2e-5 --max_seq_len 512
eval:
	python tasks/eval.py --task all
baseline:
	python tasks/train_sklearn.py --task all
ece:
	python tasks/calibration_ece.py --model_dir models/all_distilbert-base-uncased --split data/processed/test.jsonl --plot figures/ece_curve.pdf
drift:
	python tasks/continual.py --plot figures/concept_drift_sim.pdf
explain:
	python tasks/explainability.py --out reports/evidence_linked.jsonl
human:
	python tasks/human_loop.py --model_dir models/all_distilbert-base-uncased --split data/processed/test.jsonl --threshold 0.75
report:
	python tasks/report_gen.py --input data/processed/test.jsonl --out reports/test_reports.jsonl --summarizer t5-small
api:
	uvicorn apps.api:app --host 0.0.0.0 --port 8000
