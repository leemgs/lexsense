import json, argparse
from pathlib import Path
from typing import List, Dict, Any
import joblib
from sklearn.metrics import classification_report, accuracy_score
from .taxonomy import LABELS
from .preprocess import clean_text

def load_jsonl(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--model_dir", required=True)
    args = ap.parse_args()

    test = load_jsonl(Path(args.data_dir) / "test.jsonl")
    model = joblib.load(Path(args.model_dir) / "model.joblib")

    X = [clean_text(it["title"] + " " + it["body"]) for it in test]
    y = [it["category"] for it in test]
    preds = model.predict(X)
    print("TEST accuracy:", accuracy_score(y, preds))
    print(classification_report(y, preds, labels=LABELS))

if __name__ == "__main__":
    main()
