# 1) Drift detection (PSI)
```
python - <<'PY'
import numpy as np
from audits.drift_detection import population_stability_index

# e.g., scalar projections from embeddings
prev = np.random.normal(0, 1.0, size=5000)
curr = np.random.normal(0.15, 1.05, size=5000)  # small shift

res = population_stability_index(curr, prev, bins=12)
print("PSI:", res.psi, "zone:", res.zone)
PY
```

# 2) Factuality audit
```
python - <<'PY'
from audits.factuality_audit import FactualityAuditor

auditor = FactualityAuditor(
    nli_model="facebook/bart-large-mnli",
    jurisdiction_lexicon={"EU": ["EU", "European Union", "Brussels"]}
)
claims = [
    {
        "claim": "The EU AI Act was adopted in 2024 and mandates transparency obligations.",
        "evidence_span": "In 2024, the European Union adopted the AI Act, introducing transparency requirements."
    },
    {
        "claim": "The regulation reduces fines by 50%.",
        "evidence_span": "The regulation sets maximum fines up to 7% of global turnover."
    }
]
res = auditor.audit(claims)
for r in res:
    print(r)
PY
```

# 3) Paper Appendix
```
\paragraph{Supplementary Code.}
We release reference implementations for both modules introduced in Section~\ref{sec:factuality-add}:
(i) \texttt{audits/factuality_audit.py} implements our factuality audit protocol with NLI-based claim verification, numeric/date consistency checks, and minimal human-in-the-loop routing; 
(ii) \texttt{audits/drift_detection.py} provides PSI-based automated drift detection.
Example scripts and instructions are included in the repository README to reproduce auditing and drift alarms.
```

# 
