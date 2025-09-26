from typing import List, Dict

def factuality_audit(summary_sentences: List[str], evidence_spans: List[str]) -> List[Dict]:
    # Minimal stub that pairs sentences to nearest evidence span by length.
    results = []
    for i, sent in enumerate(summary_sentences):
        ev = evidence_spans[min(i, len(evidence_spans)-1)] if evidence_spans else ""
        verdict = "needs_review" if len(sent) > 300 or len(ev) == 0 else "ok"
        results.append({"sentence": sent, "evidence": ev, "confidence": 0.6 if verdict=="ok" else 0.3, "verdict": verdict})
    return results
