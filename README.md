# LexSense: Multilingual AI for Inclusive Access to Legal and Government Information

LexSense is a multilingual AI framework that helps **non-experts and multilingual
communities** access legal, regulatory, and government information that is otherwise
hard to reach because of complex terminology, fragmented sources, and language barriers.
It **collects, classifies, analyzes, and summarizes** governance-related information
across jurisdictions and languages, integrating automated change detection, multilingual
natural language processing, concept-drift monitoring, evidence-grounded analysis, and
large language model (LLM)-based reporting into a single pipeline.

This repository contains the **paper manuscript (`paper/`)** and the
**reproducibility code (`code/`)**.

---

## 📁 Repository Layout

```
lexsense/
├── README.md      # (this file) project overview and folder descriptions
├── paper/         # LaTeX manuscript
└── code/          # reproducibility code and the GovSense-1k benchmark
```

---

## 📄 `paper/` — Manuscript (LaTeX)

A LaTeX manuscript based on the Springer Nature journal template (`sn-jnl.cls`,
numbered citation style). `main.tex` assembles the paper by `\input`-ing each
section file in numeric order. The `\newcommand{\lang}{en}` value in `main.tex`
switches between the **English (en) / Korean (ko)** versions, and `\anonymous`
toggles anonymous review.

| File | Contents |
|------|----------|
| `main.tex` | Document class/packages, section assembly, hyperlink setup |
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
| `reference-data.bib` | **28 verifiable references** (each entry includes a `url` field) |
| `sn-jnl.cls`, `sn-mathphys-num.bst` | Springer Nature journal class and bibliography style |
| `fig-*.png` | Figures: system architecture, ablation, concept drift, cost–benefit |

### Blue reference URLs (pre-submission verification)
Every entry in `reference-data.bib` carries a `url` field. Combined with
`\hypersetup{colorlinks=true, urlcolor=blue}` in `main.tex`, each reference URL
prints as a **blue, clickable link**, so you can click through every citation and
confirm that the referenced paper actually exists before submission.
> For the camera-ready version, set `colorlinks=false` (or `urlcolor=black`), or
> remove the `url` fields from `reference-data.bib`.

### Building the paper (example)
```bash
cd paper
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```
> Because the manuscript supports Korean (`kotex`), XeLaTeX/LuaLaTeX or `latexmk`
> is recommended.

---

## 💻 `code/` — Implementation and the GovSense-1k Benchmark

A **reproducibility starter kit** for the pipeline described in the paper. It
includes a **synthetic benchmark** that mirrors the paper's proportions and task
setup, so the end-to-end code path can be verified without external data access.

```
code/
├── README.md                         # code usage guide (Quick Start)
├── Dockerfile                        # containerized runtime
├── pyproject.toml / requirements.txt # dependencies (pandas, numpy, scikit-learn, ...)
├── LICENSE                           # Apache-2.0
├── src/lexsense/
│   ├── taxonomy.py                   # label taxonomy and mapping
│   ├── preprocess.py                 # text cleaning and splitting
│   ├── ingest/generator_govsense.py  # GovSense-1k dataset generator
│   ├── train_classifier.py           # TF-IDF + Logistic Regression baseline (4-way)
│   ├── evaluate.py                   # metrics and report
│   ├── drift.py                      # concept-drift (PSI) utility
│   ├── audit.py                      # factuality-audit stubs
│   └── reporter.py                   # LLM report-generation stub
├── scripts/generate_govsense_1k.py   # dataset regeneration script
├── examples/demo.py                  # usage example
└── data/govsense_1k/                 # benchmark data
    ├── govsense_1k.jsonl             # full corpus (1,200 items)
    ├── train.jsonl / dev.jsonl / test.jsonl
    └── labels.csv                    # label distribution
```

### GovSense-1k benchmark
- **Size**: 1,200 items
- **Labels**: `governance` (400), `contract` (300), `lawsuit` (250), `asset` (250)
- **Languages**: primarily English (`en`), Korean (`ko`), French (`fr`), with a small
  stress subset in Spanish (`es`), Arabic (`ar`), Vietnamese (`vi`)
- **Fields**: `id`, `title`, `body`, `category`, `jurisdiction`, `language`,
  `timestamp`, `url`, `evidence_spans`

### Quick Start
```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# (optional) regenerate the synthetic GovSense-1k dataset
python scripts/generate_govsense_1k.py --out data/govsense_1k

# train and evaluate the baseline
python -m lexsense.train_classifier --data_dir data/govsense_1k --out_dir data/govsense_1k/baseline_lr
python -m lexsense.evaluate --data_dir data/govsense_1k --model_dir data/govsense_1k/baseline_lr
```

### Docker
```bash
cd code
docker build -t lexsense:starter .
docker run --rm -it -v "$PWD":/app lexsense:starter \
  python -m lexsense.train_classifier --data_dir data/govsense_1k --out_dir data/govsense_1k/baseline_lr
```

> See [`code/README.md`](code/README.md) for detailed usage.

---

## 📌 Citation

> Geunsik Lim. *LexSense: Multilingual AI for Inclusive Access to Legal and Government Information.*

## 📝 License
The code is released under the **Apache-2.0** license (see `code/LICENSE`).
