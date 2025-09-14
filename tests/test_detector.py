import os
from lexsense.changedetector import ChangeDetector

def test_fetch_changes_returns_events():
    os.environ.pop("KAFKA_BROKER", None)
    det = ChangeDetector()
    events = det.fetch_changes()
    assert isinstance(events, list) and len(events) >= 1
    for ev in events:
        assert all(k in ev for k in ("id", "title", "date"))

def test_kafka_producer_initialization(monkeypatch):
    monkeypatch.setattr('lexsense.changedetector.KafkaProducer', None)
    os.environ["KAFKA_BROKER"] = "localhost:9092"
    det = ChangeDetector()
    assert det.producer is None
