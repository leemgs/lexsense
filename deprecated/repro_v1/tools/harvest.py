#!/usr/bin/env python
import argparse, json, datetime as dt, os
def normalize(src, title, url, content="", published=""):
    return {"id": hex((hash(title)+hash(url)) & 0xffffffff)[2:], "source": src, "title": title, "url": url, "content": content, "published": published}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--toy", action="store_true")
    args = ap.parse_args()
    out = f"data/raw/harvest_{dt.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
    os.makedirs("data/raw", exist_ok=True)
    if args.toy:
        rows = [
            ("toy","EU AI Act update on transparency obligations","eu://1","category_hint:governance"),
            ("toy","Contractual clause: AI audit requirements for vendors","co://1","category_hint:contract"),
            ("toy","Lawsuit filed over unauthorized dataset usage","la://1","category_hint:lawsuit"),
            ("toy","New model release: compliance classifier weights","as://1","category_hint:asset"),
        ]
        with open(out,"w",encoding="utf-8") as f:
            for s in rows:
                f.write(json.dumps(normalize(*s), ensure_ascii=False)+"\n")
        print("[harvest] toy data ->", out)
    else:
        print("[harvest] configure real sources or use --toy")
if __name__=="__main__":
    main()
