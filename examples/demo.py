# Minimal demo showing end-to-end report rendering
from pathlib import Path
import json
from lexsense.reporter import render_structured_report

p = Path("data/govsense_1k/test.jsonl")
item = json.loads(open(p, encoding="utf-8").readline())
rep = render_structured_report(item, prediction=item["category"], confidence=0.93)
print(rep)
