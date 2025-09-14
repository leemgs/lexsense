#!/usr/bin/env python
import argparse, os, json, yaml, random, numpy as np, torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

def load_cfg(p="configs/config.yml"):
    with open(p,"r",encoding="utf-8") as f: return yaml.safe_load(f)
def read_jsonl(p): return [json.loads(l) for l in open(p,"r",encoding="utf-8")]
def set_seed(s=42):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)
    if torch.cuda.is_available(): torch.manual_seed_all(s)
def metrics(pred):
    logits, labels = pred; preds = logits.argmax(-1)
    acc = accuracy_score(labels, preds)
    p,r,f,_ = precision_recall_fscore_support(labels, preds, average="macro", zero_division=0)
    return {"accuracy":acc,"precision":p,"recall":r,"f1":f}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", default="configs/config.yml")
    ap.add_argument("--task", default="all")
    ap.add_argument("--model", default=None)
    ap.add_argument("--epochs", type=int, default=None)
    ap.add_argument("--batch", type=int, default=None)
    ap.add_argument("--lr", type=float, default=None)
    ap.add_argument("--max_seq_len", type=int, default=None)
    args = ap.parse_args()

    cfg = load_cfg(args.cfg); set_seed(cfg.get("random_seed",42))
    labels = cfg["taxonomy"]["labels"]
    model_name = args.model or cfg["training"]["default_model"]
    tr = read_jsonl("data/processed/train.jsonl"); dv=read_jsonl("data/processed/dev.jsonl"); ts=read_jsonl("data/processed/test.jsonl")
    if args.task!="all":
        sel = labels[args.task]; tr=[r for r in tr if r["label"]==sel]; dv=[r for r in dv if r["label"]==sel]; ts=[r for r in ts if r["label"]==sel]
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    def to_ds(rows): return Dataset.from_list([{"text": r["title"]+" "+r["text"], "label": r["label"]} for r in rows])
    ds_tr, ds_dv, ds_ts = to_ds(tr), to_ds(dv), to_ds(ts)
    max_len = args.max_seq_len or cfg["training"]["tasks"].get(args.task if args.task!="all" else "governance",{}).get("max_seq_len",512)
    def enc(b): return tok(b["text"], truncation=True, padding="max_length", max_length=max_len)
    ds_tr = ds_tr.map(enc, batched=True).remove_columns(["text"]).with_format("torch")
    ds_dv = ds_dv.map(enc, batched=True).remove_columns(["text"]).with_format("torch")
    ds_ts = ds_ts.map(enc, batched=True).remove_columns(["text"]).with_format("torch")
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(labels))
    tcfg = cfg["training"]["tasks"].get(args.task if args.task!="all" else "governance", {})
    epochs = args.epochs or tcfg.get("epochs",5); batch = args.batch or tcfg.get("batch_size",16); lr = args.lr or tcfg.get("lr",2e-5)
    out = f"models/{args.task}_{model_name.replace('/','-')}"; os.makedirs(out, exist_ok=True)
    targs = TrainingArguments(output_dir=out, evaluation_strategy="epoch", save_strategy="epoch", learning_rate=lr,
        per_device_train_batch_size=batch, per_device_eval_batch_size=batch, num_train_epochs=epochs, weight_decay=0.01,
        load_best_model_at_end=True, metric_for_best_model="f1", logging_dir="logs/trainer", logging_steps=10, report_to=[])
    trainer = Trainer(model=model, args=targs, train_dataset=ds_tr, eval_dataset=ds_dv, tokenizer=tok, compute_metrics=metrics)
    trainer.train(); m = trainer.evaluate(ds_ts)
    with open(os.path.join(out,"test_metrics.json"),"w") as f: json.dump(m,f,indent=2)
    print("[test]", m)
if __name__=="__main__":
    main()
