# LexSense — Manuscript (`paper/`)

LaTeX sources for the paper:

> **LexSense: Multilingual AI for Inclusive Access to Legal and Government Information**

The manuscript uses the Springer Nature journal template (`sn-jnl.cls`) with the
numbered math/physics citation style (`sn-mathphys-num.bst`). `main.tex` assembles
the paper by `\input`-ing each section file in numeric order.

---

## 📂 Files

| File | Contents |
|------|----------|
| `main.tex` | Document class, packages, hyperlink setup, and section assembly |
| `001_title.tex` | Paper title |
| `005_author.tex` | Authors and affiliations |
| `010_abstract.tex` | Abstract and keywords (EN/KO) |
| `020_introduction.tex` | Introduction — problem framing and contributions |
| `040_background.tex` | Background — prior approaches, multilingual NLP/LLMs, research gap |
| `050_design.tex` | LexSense design and implementation (5-module architecture) |
| `065_evaluation.tex` | Evaluation — dataset, metrics, quantitative results, ablation |
| `067_extended_evaluation.tex` | Extended evaluation — concept drift, evidence-linked explainability, cross-lingual stress tests, factuality audit |
| `070_discussion.tex` | Discussion — strengths, limitations, threats to validity, case snapshots |
| `075_ethical_impact.tex` | Ethical and societal impact — fairness, transparency, privacy |
| `080_related_work.tex` | Related work |
| `085_limitation.tex` | Limitations and future directions |
| `090_conclusion.tex` | Conclusion |
| `095_reference.tex` | Bibliography loader (`\bibliography{reference-data}`) |
| `reference-data.bib` | 28 verifiable references, each with a `url` field |
| `sn-jnl.cls`, `sn-mathphys-num.bst` | Springer Nature journal class and bibliography style |
| `fig-system_architecture.png` | System architecture (5 modules) |
| `fig-ablation_study.png` | Ablation study results |
| `fig-concept_drift.png` | Concept drift and recovery (Macro-F1) |
| `fig-cost_benefit.png` | Accuracy vs. review-cost utility curve |

> `note/` and `trash/` hold scratch/legacy material and are not part of the build.

---

## 🌐 Language and anonymity toggles

Both switches live near the top of `main.tex`:

```latex
\newcommand{\lang}{en}        % en = English, ko = Korean
\newcommand{\anonymous}{false} % true = anonymized author block
```

Every section file contains both an English and a Korean version guarded by
`\ifthenelse{\equal{\lang}{ko}}{ ... KO ... }{ ... EN ... }`, so changing `\lang`
switches the whole paper's language.

---

## 🔗 Blue reference URLs (pre-submission verification)

Every entry in `reference-data.bib` carries a `url` field, and `main.tex` sets:

```latex
\hypersetup{colorlinks=true, urlcolor=blue, linkcolor=black, citecolor=black}
```

As a result, each reference URL prints as a **blue, clickable link** while
citations and internal links stay black. This lets you click through every
reference and confirm the cited paper actually exists before submission.

**For the camera-ready version**, do one of:
- set `colorlinks=false` (or `urlcolor=black`) in `main.tex`, and/or
- remove the `url` fields from `reference-data.bib`.

---

## 🛠 Building the PDF

```bash
cd paper
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

Because the manuscript supports Korean (`kotex`), **XeLaTeX or LuaLaTeX** is
recommended; `latexmk` also works:

```bash
# XeLaTeX route (handles kotex well)
latexmk -xelatex main.tex

# or pdfLaTeX route
latexmk -pdf main.tex
```

Outputs `main.pdf` in this folder.

---

## ✅ Reference sanity check

The bibliography is kept in sync with the in-text citations: there are exactly
28 entries and all of them are cited (no undefined and no uncited references).
When editing, you can re-verify with:

```bash
cd paper
# cited keys
grep -rho '\cite{[^}]*}' 0*.tex | sed 's/\\cite{//;s/}//' | tr ',' '\n' \
  | sed 's/ //g' | sort -u > /tmp/cited.txt
# bib keys
grep -oE '^@[a-zA-Z]+\{[^,]+' reference-data.bib | sed 's/^@[a-zA-Z]*{//' | sort -u > /tmp/bibkeys.txt
diff /tmp/cited.txt /tmp/bibkeys.txt && echo "OK: cited keys == bib keys"
```
