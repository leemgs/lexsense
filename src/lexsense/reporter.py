from typing import Dict

def render_structured_report(item: Dict, prediction: str, confidence: float) -> Dict:
    # Simple structured report; in practice, plug an LLM to expand these fields.
    return {
        "title": item.get("title"),
        "detected_category": prediction,
        "confidence": round(confidence, 3),
        "jurisdiction": item.get("jurisdiction"),
        "language": item.get("language"),
        "timestamp": item.get("timestamp"),
        "url": item.get("url"),
        "provenance": item.get("evidence_spans", [])[:3],
        "summary": f"This document appears to be {prediction} relevant. Source: {item.get('url', 'N/A')}."
    }
