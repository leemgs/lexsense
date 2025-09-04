#!/usr/bin/env python
import argparse, json, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
def split_sents(t): 
    t=t.replace("?",".").replace("!",".");
    return [s.strip() for s in t.split(".") if s.strip()]
def tfidf_rationale(sents, k=2):
    vec=TfidfVectorizer(); X=vec.fit_transform(sents); sc=X.max(axis=1).A.ravel(); idx=np.argsort(-sc)[:k]; return [sents[i] for i in idx]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--split", default="data/processed/test.jsonl"); ap.add_argument("--out", default="reports/evidence_linked.jsonl"); args=ap.parse_args()
    rows=[json.loads(l) for l in open(args.split,"r",encoding="utf-8")]; out=[]
    for r in rows:
        sents=split_sents((r.get('title','')+'. '+r.get('text','')).strip()); out.append({"id":r["id"],"title":r["title"],"label_name":r["label_name"],"rationale":tfidf_rationale(sents,2),"provenance":r.get("provenance",{})})
    import os; os.makedirs("reports", exist_ok=True)
    with open(args.out,"w",encoding="utf-8") as f:
        for o in out: f.write(json.dumps(o, ensure_ascii=False)+"\n")
    print("[explain]", len(out), "items ->", args.out)
if __name__=="__main__": main()
