"""Change Detector – simulates monitoring of regulatory updates and emits events."""
import os, json
from datetime import datetime
try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None

class ChangeDetector:
    def __init__(self, kafka_broker: str | None = None) -> None:
        if kafka_broker is None:
            kafka_broker = os.getenv("KAFKA_BROKER")
        self.kafka_broker = kafka_broker
        self.producer = None
        if kafka_broker and KafkaProducer is not None:
            try:
                self.producer = KafkaProducer(bootstrap_servers=kafka_broker,
                                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            except Exception as e:
                print(f"[ChangeDetector] Kafka init failed: {e}")
                self.producer = None
        self.sample_events = [
            {"id": "doc1", "title": "EU AI Act Passed", "source": "Gov Portal", "date": "2023-06-14"},
            {"id": "doc2", "title": "Contract Clause on Data Privacy", "source": "Contract DB", "date": "2023-09-01"},
            {"id": "doc3", "title": "Lawsuit: Jane Doe vs TechCorp", "source": "Court Filings", "date": "2024-01-05"},
            {"id": "doc4", "title": "AI Model GPT-5 Released", "source": "Tech News", "date": "2025-03-01"}
        ]

    def fetch_changes(self) -> list[dict]:
        out = []
        for ev in self.sample_events:
            out.append(ev)
            if self.producer:
                try:
                    msg = ev | {"timestamp": datetime.utcnow().isoformat()}
                    self.producer.send("changes", msg)
                except Exception as e:
                    print(f"[ChangeDetector] Kafka send failed: {e}")
        if self.producer:
            try:
                self.producer.flush(timeout=5)
            except Exception as e:
                print(f"[ChangeDetector] Kafka flush error: {e}")
        return out
