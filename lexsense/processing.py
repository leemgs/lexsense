"""Processing & Analysis – classification + entity extraction."""
import os, re
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

class NLPProcessor:
    def __init__(self) -> None:
        self.testing = os.getenv("TESTING") == "1"
        self.taxonomy_keywords = {
            "Contract": ["contract", "clause", "party"],
            "Lawsuit": ["lawsuit", "plaintiff", " vs", "court"],
            "AI Release": ["model release", "model released", "released the model", "release notes"],
            "Regulation": [" act", "guideline", "regulation", " law"]
        }
        self.ner = None
        if not self.testing and pipeline is not None:
            try:
                self.ner = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER")
            except Exception as e:
                print(f"[NLPProcessor] NER init failed: {e}")
                self.ner = None
        self.p_multi = re.compile(r"\b([A-Z][A-Za-z0-9&\.-]+(?:\s+[A-Z][A-Za-z0-9&\.-]+)+)\b")
        self.p_company = re.compile(r"\b[A-Z][A-Za-z]*?(?:Corp|Inc|Ltd|LLC)\b")
        self.p_acronym = re.compile(r"\b[A-Z]{2,}\b")

    def classify_text(self, text: str) -> str:
        tl = text.lower()
        for cat, kws in self.taxonomy_keywords.items():
            for kw in kws:
                if kw in tl:
                    return cat
        return "Other"

    def extract_entities(self, text: str) -> list[str]:
        entities: list[str] = []
        if self.ner and not self.testing:
            try:
                for ent in self.ner(text):
                    label = ent.get("word") or ent.get("entity") or ""
                    if label:
                        entities.append(label.strip())
            except Exception as e:
                print(f"[NLPProcessor] NER failed, using regex: {e}")
                self.ner = None
        if self.ner is None or self.testing:
            cands: list[tuple[int, str]] = []
            for m in self.p_multi.finditer(text):
                cands.append((m.start(), m.group().strip()))
            for m in self.p_company.finditer(text):
                cands.append((m.start(), m.group().strip()))
            for m in self.p_acronym.finditer(text):
                ac = m.group().strip()
                if ac in ("AI",):
                    continue
                cands.append((m.start(), ac))
            cands.sort(key=lambda x: x[0])
            for _, ent in cands:
                entities.append(ent)
        seen = set(); uniq = []
        for e in entities:
            if e not in seen:
                seen.add(e); uniq.append(e)
        return uniq

    def analyze(self, text: str) -> dict:
        return {"category": self.classify_text(text), "entities": self.extract_entities(text)}
