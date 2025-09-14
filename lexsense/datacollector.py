"""Data Collector – loads source documents (demo uses local files)."""
import os
from pathlib import Path

class DataCollector:
    def __init__(self) -> None:
        self.sample_dir = Path(__file__).resolve().parent / "sample_data"

    def collect(self, event: dict) -> dict:
        doc_id = event.get("id")
        result = {"id": doc_id, "title": event.get("title"), "date": event.get("date"), "source": event.get("source")}
        text = ""
        if doc_id:
            fp = self.sample_dir / f"{doc_id}.txt"
            if fp.exists():
                text = fp.read_text(encoding="utf-8")
        result["text"] = text
        return result
