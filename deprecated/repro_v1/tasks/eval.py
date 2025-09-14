#!/usr/bin/env python
import argparse, json, yaml
from sklearn.metrics import classification_report, confusion_matrix
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
def load_cfg(p="configs/config.yml"):
    with open(p,"r",encoding="utf-8") as f: return yaml.safe_load(f)
def read_jsonl(p): return [json.loads(l) for l in open(p,"r",encoding="utf-8")]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--cfg", default="configs/config.yml"); ap.add_argument("--task", default="all"); ap.add_argument("--model_dir", default=None); args=ap.parse_args()
    cfg=load_cfg(args.cfg); labels=cfg["taxonomy"]["labels"]
    ts=read_jsonl("data/processed/test.jsonl"); 
    if args.task!="all": sel=labels[args.task]; ts=[r for r in ts if r["label"]==sel]
    if not args.model_dir:
        import glob; cands=glob.glob("models/*"); args.model_dir=sorted(cands)[-1]
    tok=AutoTokenizer.from_pretrained(args.model_dir); mdl=AutoModelForSequenceClassification.from_pretrained(args.model_dir); mdl.eval()
    texts=[r["title"]+" "+r["text"] for r in ts]; y=[r["label"] for r in ts]; preds=[]
    for i in range(0,len(texts),8):
        enc=tok(texts[i:i+8], truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad(): logits=mdl(**enc).logits
        preds+=logits.argmax(-1).cpu().tolist()
    print(classification_report(y, preds))
    print("Confusion matrix:\n", confusion_matrix(y, preds))
if __name__=="__main__":
    main()
