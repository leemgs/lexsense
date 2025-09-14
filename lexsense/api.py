"""FastAPI backend – runs the pipeline once on startup and serves results."""
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from lexsense.changedetector import ChangeDetector
from lexsense.datacollector import DataCollector
from lexsense.processing import NLPProcessor
from lexsense.reporter import Reporter

detector = ChangeDetector()
collector = DataCollector()
processor = NLPProcessor()
reporter = Reporter()

reports_data: List[dict] = []

app = FastAPI(title="LexSense API", version="0.1")

class Report(BaseModel):
    id: str
    title: str
    date: str
    source: str
    category: str
    entities: List[str]
    summary: str

@app.on_event("startup")
def startup_event():
    global reports_data
    events = detector.fetch_changes()
    out = []
    for ev in events:
        doc = collector.collect(ev)
        txt = doc.get("text", "")
        if txt:
            doc.update(processor.analyze(txt))
            doc["summary"] = reporter.summarize(txt)
        else:
            doc["category"] = "N/A"
            doc["entities"] = []
            doc["summary"] = ""
        out.append(doc)
    reports_data = out
    print(f"[startup] Processed {len(reports_data)} documents.")

@app.get("/reports", response_model=List[Report])
def get_reports():
    return reports_data

@app.get("/reports/{doc_id}")
def get_report_detail(doc_id: str):
    for d in reports_data:
        if d.get("id") == doc_id:
            return {
                "id": d["id"], "title": d["title"], "date": d["date"], "source": d["source"],
                "category": d.get("category", ""), "entities": d.get("entities", []),
                "summary": d.get("summary", ""), "text": d.get("text", "")
            }
    return {"error": "Document not found"}
