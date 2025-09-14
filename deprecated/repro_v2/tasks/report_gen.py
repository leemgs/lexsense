#!/usr/bin/env python
import argparse, json
from transformers import pipeline
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--input", required=True); ap.add_argument("--out", required=True); ap.add_argument("--summarizer", default="t5-small"); args=ap.parse_args()
    rows=[json.loads(l) for l in open(args.input,"r",encoding="utf-8")]
    texts=[(r.get("title","")+". "+r.get("text","")).strip()[:2000] for r in rows]
    pipe=pipeline("summarization", model=args.summarizer); outs=pipe(texts, truncation=True)
    import os; os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out,"w",encoding="utf-8") as f:
        for r,o in zip(rows,outs):
            f.write(json.dumps({"id":r["id"],"title":r["title"],"label_name":r["label_name"],"summary":o["summary_text"],"provenance":r.get("provenance",{})}, ensure_ascii=False)+"\n")
    print("[report]", len(rows), "summaries ->", args.out)
if __name__=="__main__": main()
