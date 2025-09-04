#!/usr/bin/env python
import argparse, json, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
def read_jsonl(p): return [json.loads(l) for l in open(p,"r",encoding="utf-8")]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--model_dir", required=True); ap.add_argument("--split", default="data/processed/test.jsonl"); ap.add_argument("--threshold", type=float, default=0.75); args=ap.parse_args()
    rows=read_jsonl(args.split); texts=[r["title"]+" "+r["text"] for r in rows]; y=np.array([r["label"] for r in rows])
    tok=AutoTokenizer.from_pretrained(args.model_dir); mdl=AutoModelForSequenceClassification.from_pretrained(args.model_dir); mdl.eval()
    probs=[]; preds=[]
    for i in range(0,len(texts),8):
        enc=tok(texts[i:i+8], truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad(): logits=mdl(**enc).logits
        p=torch.softmax(logits, dim=-1); conf, cls = p.max(-1)
        probs+=conf.cpu().tolist(); preds+=cls.cpu().tolist()
    probs=np.array(probs); preds=np.array(preds); low=probs<args.threshold; rate=low.mean()
    corrected=preds.copy(); corrected[low]=y[low]
    before=(preds==y).mean(); after=(corrected==y).mean()
    print(f"Flagged: {rate*100:.1f}% | accuracy {before:.3f} -> {after:.3f}")
if __name__=="__main__": main()
