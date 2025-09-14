#!/usr/bin/env python
import argparse, json, numpy as np, matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
def read_jsonl(p): return [json.loads(l) for l in open(p,"r",encoding="utf-8")]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--model_dir", required=True); ap.add_argument("--split", default="data/processed/test.jsonl"); ap.add_argument("--plot", default=None); args=ap.parse_args()
    rows=read_jsonl(args.split); texts=[r["title"]+" "+r["text"] for r in rows]; y=np.array([r["label"] for r in rows])
    tok=AutoTokenizer.from_pretrained(args.model_dir); mdl=AutoModelForSequenceClassification.from_pretrained(args.model_dir); mdl.eval()
    probs=[]; preds=[]
    for i in range(0,len(texts),8):
        enc=tok(texts[i:i+8], truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad(): logits=mdl(**enc).logits
        p=torch.softmax(logits, dim=-1).max(-1).values.cpu().numpy(); probs+=p.tolist(); preds+=logits.argmax(-1).cpu().tolist()
    probs=np.array(probs); correct=(np.array(preds)==y).astype(float)
    bins=np.linspace(0,1,11); ece=0.0
    for b in range(10):
        idx=(probs>=bins[b]) & (probs<bins[b+1])
        if idx.any(): ece += idx.mean() * abs(probs[idx].mean() - correct[idx].mean())
    print(f"ECE(10bins)={ece:.4f}")
    if args.plot:
        centers=0.5*(bins[1:]+bins[:-1]); accs=[]; 
        for b in range(10):
            idx=(probs>=bins[b]) & (probs<bins[b+1])
            accs.append(correct[idx].mean() if idx.any() else 0)
        plt.figure(); plt.plot([0,1],[0,1]); plt.plot(centers, accs, marker='o'); plt.xlabel('Confidence'); plt.ylabel('Accuracy'); plt.title('Reliability Diagram'); plt.tight_layout(); plt.savefig(args.plot); print('[plot]', args.plot)
if __name__=="__main__": main()
