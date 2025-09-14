# audits/factuality_audit.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import re
import numpy as np
from rapidfuzz import fuzz
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

@dataclass
class ClaimAudit:
    claim: str
    evidence_span: str
    confidence: float
    verdict: str  # "supported" | "contradicted" | "uncertain"
    numeric_ok: bool
    date_ok: bool
    jurisdiction_ok: bool
    notes: Optional[str] = None

class FactualityAuditor:
    """
    Minimal factuality audit protocol:
    1) Source alignment: claim -> evidence span
    2) Claim verification: NLI (entail/contradict/neutral) + numeric/date checks
    3) Minimal human-in-the-loop: low-confidence routing
    """

    def __init__(
        self,
        nli_model: str = "facebook/bart-large-mnli",  # multilingual: "joeddav/xlm-roberta-large-xnli"
        jurisdiction_lexicon: Optional[Dict[str, List[str]]] = None,
        device: Optional[str] = None,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(nli_model)
        self.model = AutoModelForSequenceClassification.from_pretrained(nli_model)
        self.model.eval()
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # e.g., {"EU": ["EU", "European Union", "Brussels"], "US": ["US", "USA", "United States"]}
        self.jurisdiction_lexicon = jurisdiction_lexicon or {}

        # label mapping for BART NLI
        self.entail_id = self.model.config.label2id.get("ENTAILMENT", 2)
        self.contra_id = self.model.config.label2id.get("CONTRADICTION", 0)
        self.neutral_id = self.model.config.label2id.get("NEUTRAL", 1)

    @staticmethod
    def _extract_numbers(text: str) -> List[str]:
        # captures integers, floats, percentages, date-like (YYYY or YYYY-MM-DD)
        return re.findall(r"\b(?:\d{4}(?:-\d{2}-\d{2})?|\d+(?:\.\d+)?%?)\b", text)

    @staticmethod
    def _jurisdiction_ok(claim: str, evidence: str, lex: Dict[str, List[str]]) -> bool:
        if not lex:
            return True
        def has_token(s, toks): 
            return any(t in s for t in toks)
        for region, toks in lex.items():
            in_claim = has_token(claim, toks)
            in_evid = has_token(evidence, toks)
            if in_claim and not in_evid:
                return False
        return True

    @torch.no_grad()
    def _nli_score(self, premise: str, hypothesis: str) -> Dict[str, float]:
        # premise = evidence, hypothesis = claim
        inputs = self.tokenizer(
            premise, hypothesis, return_tensors="pt",
            truncation=True, max_length=512
        ).to(self.device)
        logits = self.model(**inputs).logits[0].float()
        probs = torch.softmax(logits, dim=-1).detach().cpu().numpy()
        return {
            "entail": float(probs[self.entail_id]),
            "contradict": float(probs[self.contra_id]),
            "neutral": float(probs[self.neutral_id]),
        }

    @staticmethod
    def _numeric_and_date_ok(claim: str, evidence: str) -> (bool, bool):
        nums_c = set(FactualityAuditor._extract_numbers(claim))
        nums_e = set(FactualityAuditor._extract_numbers(evidence))

        # if claim has numbers but evidence doesn't -> fail
        numeric_ok = True
        date_ok = True

        # numeric consistency: rough check via string equality or high similarity
        for n in nums_c:
            if "%" in n or re.match(r"^\d+(\.\d+)?$", n):
                # allow fuzzy match to tolerate formatting (e.g., 70 vs 70.0)
                matched = any(n == m or fuzz.ratio(n, m) >= 95 for m in nums_e)
                if not matched:
                    numeric_ok = False

            # date pattern YYYY or YYYY-MM-DD
            if re.match(r"^\d{4}(-\d{2}-\d{2})?$", n):
                matched = any(n == m for m in nums_e)
                if not matched:
                    date_ok = False

        return numeric_ok, date_ok

    def audit(
        self,
        claims_with_evidence: List[Dict[str, Any]],
        low_conf_threshold: float = 0.75,
    ) -> List[ClaimAudit]:
        """
        claims_with_evidence: list of {"claim": str, "evidence_span": str}
        """
        results: List[ClaimAudit] = []
        for item in claims_with_evidence:
            claim = item["claim"].strip()
            evidence = item["evidence_span"].strip()

            # 1) NLI score
            nli = self._nli_score(premise=evidence, hypothesis=claim)
            confidence = max(nli["entail"], nli["contradict"])

            # 2) numeric/date checks
            numeric_ok, date_ok = self._numeric_and_date_ok(claim, evidence)

            # 3) jurisdiction consistency
            juris_ok = self._jurisdiction_ok(claim, evidence, self.jurisdiction_lexicon)

            # verdict
            if nli["entail"] >= 0.5 and numeric_ok and date_ok and juris_ok:
                verdict = "supported"
            elif nli["contradict"] >= 0.5:
                verdict = "contradicted"
            else:
                verdict = "uncertain"

            notes = None
            if confidence < low_conf_threshold:
                notes = "low-confidence: route for partial human review"

            results.append(ClaimAudit(
                claim=claim,
                evidence_span=evidence,
                confidence=confidence,
                verdict=verdict,
                numeric_ok=numeric_ok,
                date_ok=date_ok,
                jurisdiction_ok=juris_ok,
                notes=notes,
            ))
        return results
