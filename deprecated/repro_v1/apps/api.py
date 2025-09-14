from fastapi import FastAPI
import os, json
app = FastAPI(title="AI Trend Sensing API")
@app.get("/healthz")
def health(): return {"status":"ok"}
@app.get("/items")
def items(split: str="test", limit: int=10):
    path=os.path.join("data/processed", f"{split}.jsonl"); out=[]
    try:
        with open(path,"r",encoding="utf-8") as f:
            for i,line in enumerate(f):
                if i>=limit: break
                out.append(json.loads(line))
    except FileNotFoundError:
        return {"error": f"not found: {path}"}
    return {"items": out}
