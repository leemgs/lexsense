import os
from lexsense.reporter import Reporter
os.environ['TESTING'] = '1'

def test_summarize_simple():
    rep = Reporter()
    text = "This is a long document. It has multiple sentences. It should be summarized."
    summary = rep.summarize(text)
    assert isinstance(summary, str) and summary != "" and len(summary) < len(text)
