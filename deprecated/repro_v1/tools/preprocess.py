#!/usr/bin/env python
import argparse, os, json, random, re, yaml
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 42
def load_cfg(p="configs/config.yml"):
    with open(p,"r",encoding="utf-8") as f: return yaml.safe_load(f)
def norm(s): return re.sub(r"\s+"," ", (s or "").strip())
def infer(title, text):
    t=(title+" "+text).lower()
    if "category_hint:" in t: return t.split("category_hint:")[1].split()[0]
    if any(k in t for k in ["lawsuit","court","ruling","class action"]): return "lawsuit"
    if any(k in t for k in ["contract","clause","msa","dpa","scc"]): return "contract"
    if any(k in t for k in ["model release","dataset release","weights","asset"]): return "asset"
    return "governance"
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--cfg", default="configs/config.yml"); args=ap.parse_args()
    cfg=load_cfg(args.cfg); labels=cfg["taxonomy"]["labels"]
    rows=[]
    if os.path.isdir("data/raw"):
        for fn in os.listdir("data/raw"):
            if fn.endswith(".jsonl"):
                for line in open(os.path.join("data/raw",fn),"r",encoding="utf-8"):
                    try: rows.append(json.loads(line))
                    except: pass
    # plus bundled sample
    sample_path="data/raw/harvest_sample.jsonl"
    if os.path.exists(sample_path):
        for line in open(sample_path,"r",encoding="utf-8"):
            rows.append(json.loads(line))
    # dedup
    seen=set(); uniq=[]
    for r in rows:
        k=r.get("url") or r.get("title")
        if not k or k in seen: continue
        seen.add(k); uniq.append(r)
    ds=[]
    for r in uniq:
        title=norm(r.get("title","")); text=norm(r.get("content","")) or title
        try: lang=detect(title or text)
        except: lang="unk"
        name=infer(title,text); ds.append({"id":r.get("id"),"title":title,"text":text,"lang":lang,"label":labels[name],"label_name":name,"provenance":{"url":r.get("url")}})
    random.seed(42); random.shuffle(ds); n=len(ds); ntr=int(0.7*n); nd=int(0.15*n)
    splits={"train":ds[:ntr], "dev":ds[ntr:ntr+nd], "test":ds[ntr+nd:]}
    os.makedirs("data/processed", exist_ok=True)
    for k,v in splits.items():
        with open(f"data/processed/{k}.jsonl","w",encoding="utf-8") as f:
            for x in v: f.write(json.dumps(x, ensure_ascii=False)+"\n")
    with open("data/processed/labels.json","w") as f: json.dump(labels,f,indent=2)
    print("[preprocess]", {k:len(v) for k,v in splits.items()})
if __name__=="__main__":
    main()
