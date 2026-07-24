# LexSense: 법률·정부 정보에 대한 포용적 접근을 위한 다국어 AI

> **LexSense: Multilingual AI for Inclusive Access to Legal and Government Information**

LexSense는 복잡한 전문 용어, 파편화된 출처, 언어 장벽으로 인해 법률·규제·정부 정보에 접근하기 어려운
**비전문가와 다국어 공동체**를 지원하기 위한 다국어 AI 프레임워크입니다.
다양한 관할권과 언어에 걸쳐 거버넌스 관련 정보를 **수집·분류·분석·요약**하며,
자동 변화 탐지, 다국어 자연어 처리, 개념 드리프트(concept drift) 모니터링,
근거 기반(evidence-grounded) 분석, 대규모 언어 모델(LLM) 기반 보고를 하나의 파이프라인으로 통합합니다.

이 저장소는 **논문 원고(`paper/`)** 와 **재현용 구현 코드(`code/`)** 로 구성됩니다.

---

## 📁 저장소 구조

```
lexsense/
├── README.md      # (본 파일) 프로젝트 개요 및 폴더 설명
├── paper/         # LaTeX 기반 논문 원고
└── code/          # 재현용 구현 코드 및 GovSense-1k 벤치마크
```

---

## 📄 `paper/` — 논문 원고 (LaTeX)

Springer Nature 저널 템플릿(`sn-jnl.cls`, 수치형 인용 스타일)을 사용하는 LaTeX 원고입니다.
`main.tex`가 각 절(section) 파일을 번호 순서대로 `\input` 하여 하나의 논문으로 조립합니다.
`main.tex`의 `\newcommand{\lang}{en}` 값으로 **영어(en)/한국어(ko)** 버전을 전환할 수 있으며,
`\anonymous` 값으로 익명 심사 여부를 전환합니다.

| 파일 | 내용 |
|------|------|
| `main.tex` | 문서 클래스·패키지 설정, 절 조립, 하이퍼링크 설정 |
| `001_title.tex` | 논문 제목 |
| `005_author.tex` | 저자 및 소속 정보 |
| `010_abstract.tex` | 초록 및 키워드 (영/한) |
| `020_introduction.tex` | 서론 — 정보 접근성 문제 정의 및 기여 |
| `040_background.tex` | 배경 — 기존 접근법, 다국어 NLP/LLM, 연구 공백 |
| `050_design.tex` | LexSense 설계 및 구현 (5개 모듈 아키텍처) |
| `065_evaluation.tex` | 평가 — 데이터셋, 지표, 정량 결과, 소거(ablation) 연구 |
| `067_extended_evaluation.tex` | 확장 평가 — 개념 드리프트, 근거 기반 설명 가능성, 다국어 스트레스 테스트, 사실성 감사 |
| `070_discussion.tex` | 논의 — 강점, 한계, 타당성 위협, 사례 스냅샷 |
| `075_ethical_impact.tex` | 윤리적·사회적 영향 — 공정성, 투명성, 프라이버시 |
| `080_related_work.tex` | 관련 연구 |
| `085_limitation.tex` | 한계 및 향후 연구 방향 |
| `090_conclusion.tex` | 결론 |
| `095_reference.tex` | 참고문헌 로딩(`\bibliography{reference-data}`) |
| `reference-data.bib` | **28개의 검증 가능한 참고문헌**(각 항목에 `url` 필드 포함) |
| `sn-jnl.cls`, `sn-mathphys-num.bst` | Springer Nature 저널 클래스·서지 스타일 |
| `fig-*.png` | 시스템 아키텍처, 소거 연구, 개념 드리프트, 비용–편익 그림 |

### 참고문헌 URL 파랑색 출력(제출 전 검증용)
`reference-data.bib`의 모든 항목에는 `url` 필드가 있으며,
`main.tex`의 `\hypersetup{colorlinks=true, urlcolor=blue}` 설정에 따라
참고문헌의 URL이 **파랑색 클릭 가능한 링크**로 출력됩니다.
이를 통해 제출 전에 각 인용 논문이 실제로 존재하는지 클릭하여 확인할 수 있습니다.
> 카메라레디(최종본)에서는 `colorlinks=false`(또는 `urlcolor=black`)로 바꾸거나
> `reference-data.bib`의 `url` 필드를 제거하면 됩니다.

### 논문 빌드 (예시)
```bash
cd paper
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```
> 한국어(`kotex`) 지원을 위해 XeLaTeX/LuaLaTeX 또는 `latexmk` 사용을 권장합니다.

---

## 💻 `code/` — 구현 및 GovSense-1k 벤치마크

논문에서 설명한 파이프라인의 **재현용 스타터 키트**입니다.
외부 데이터 접근 없이 엔드투엔드 코드 경로를 검증할 수 있도록,
논문과 동일한 비율·과제 설정을 따르는 **합성(synthetic) 벤치마크**를 포함합니다.

```
code/
├── README.md                         # 코드 사용 안내(Quick Start)
├── Dockerfile                        # 컨테이너 실행 환경
├── pyproject.toml / requirements.txt # 의존성 (pandas, numpy, scikit-learn 등)
├── LICENSE                           # Apache-2.0
├── src/lexsense/
│   ├── taxonomy.py                   # 라벨 분류체계 및 매핑
│   ├── preprocess.py                 # 텍스트 정제 및 분할
│   ├── ingest/generator_govsense.py  # GovSense-1k 데이터 생성기
│   ├── train_classifier.py           # TF-IDF + 로지스틱 회귀 베이스라인(4-way 분류)
│   ├── evaluate.py                   # 지표 계산 및 리포트
│   ├── drift.py                      # 개념 드리프트(PSI) 유틸리티
│   ├── audit.py                      # 사실성 감사(factuality audit) 스텁
│   └── reporter.py                   # LLM 보고 생성 스텁
├── scripts/generate_govsense_1k.py   # 데이터셋 재생성 스크립트
├── examples/demo.py                  # 사용 예시
└── data/govsense_1k/                 # 벤치마크 데이터
    ├── govsense_1k.jsonl             # 전체 코퍼스(1,200건)
    ├── train.jsonl / dev.jsonl / test.jsonl
    └── labels.csv                    # 라벨 분포
```

### GovSense-1k 벤치마크
- **규모**: 1,200건
- **라벨**: `governance`(400), `contract`(300), `lawsuit`(250), `asset`(250)
- **언어**: 주로 영어(`en`)·한국어(`ko`)·프랑스어(`fr`), 소규모 스트레스 세트로 스페인어(`es`)·아랍어(`ar`)·베트남어(`vi`)
- **필드**: `id`, `title`, `body`, `category`, `jurisdiction`, `language`, `timestamp`, `url`, `evidence_spans`

### 빠른 시작 (Quick Start)
```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# (선택) 합성 GovSense-1k 데이터 재생성
python scripts/generate_govsense_1k.py --out data/govsense_1k

# 베이스라인 학습 및 평가
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

> 자세한 코드 사용법은 [`code/README.md`](code/README.md)를 참고하세요.

---

## 📌 인용

> Geunsik Lim. *LexSense: Multilingual AI for Inclusive Access to Legal and Government Information.*

## 📝 라이선스
코드는 **Apache-2.0** 라이선스를 따릅니다(`code/LICENSE` 참고).
