#!/usr/bin/env python
import argparse, json, yaml, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
def load_cfg(p="configs/config.yml"):
    with open(p,"r",encoding="utf-8") as f: return yaml.safe_load(f)
def read_jsonl(p): return [json.loads(l) for l in open(p,"r",encoding="utf-8")]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--cfg", default="configs/config.yml"); ap.add_argument("--task", default="all"); args=ap.parse_args()
    cfg=load_cfg(args.cfg); labels=cfg["taxonomy"]["labels"]
    tr=read_jsonl("data/processed/train.jsonl"); ts=read_jsonl("data/processed/test.jsonl")
    if args.task!="all": sel=labels[args.task]; tr=[r for r in tr if r["label"]==sel]; ts=[r for r in ts if r["label"]==sel]
    Xtr=[r["title"]+" "+r["text"] for r in tr]; ytr=[r["label"] for r in tr]; Xts=[r["title"]+" "+r["text"] for r in ts]; yts=[r["label"] for r in ts]
    pipe=Pipeline([("tfidf", TfidfVectorizer(max_features=50000)), ("lr", LogisticRegression(max_iter=300))]); pipe.fit(Xtr,ytr)
    preds=pipe.predict(Xts); print(classification_report(yts,preds))
    os.makedirs("models", exist_ok=True); joblib.dump(pipe, f"models/baseline_logreg_{args.task}.joblib")
if __name__=="__main__":
    main()
