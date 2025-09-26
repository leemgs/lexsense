import json, argparse, os
from pathlib import Path
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
from .taxonomy import LABELS, LABEL_TO_ID
from .preprocess import clean_text

def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    train = load_jsonl(data_dir / "train.jsonl")
    dev = load_jsonl(data_dir / "dev.jsonl")

    def to_xy(items):
        X = [clean_text(it["title"] + " " + it["body"]) for it in items]
        y = [it["category"] for it in items]
        return X, y

    X_train, y_train = to_xy(train)
    X_dev, y_dev = to_xy(dev)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=200))
    ])

    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_dev)
    print("DEV accuracy:", accuracy_score(y_dev, preds))
    print(classification_report(y_dev, preds, labels=LABELS))

    joblib.dump(pipe, out_dir / "model.joblib")
    with open(out_dir / "labels.txt", "w") as f:
        f.write("\n".join(LABELS))

if __name__ == "__main__":
    main()
