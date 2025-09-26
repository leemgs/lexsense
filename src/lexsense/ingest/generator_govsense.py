import argparse, json, random, os
from pathlib import Path
from datetime import datetime, timedelta
random.seed(1337)

CATS = [("governance", 400), ("contract", 300), ("lawsuit", 250), ("asset", 250)]
JURIS = ["EU", "US", "KR", "FR"]
LANGS_MAIN = ["en", "ko", "fr"]
LANGS_STRESS = ["es", "ar", "vi"]  # small subset for stress test

GOV_TITLES_EN = [
    "AI Act Guidance Released", "New Transparency Rules Proposed",
    "Ethical AI Guidelines Updated", "Risk Management Directive Draft"
]
CONTRACT_TITLES_EN = [
    "Data Processing Addendum for LLM Providers",
    "AI Vendor MSA Amendment: Audit & Logs",
    "Cross-border Transfer Clause: Model Artifacts"
]
LAWSUIT_TITLES_EN = [
    "Class Action Filed over AI Training Data",
    "Injunction Sought against Model Deployment",
    "Copyright Dispute on Synthetic Data"
]
ASSET_TITLES_EN = [
    "Release Notes: LLM-4.1 Safety Update",
    "New Dataset: Multilingual Governance Corpus",
    "Bugfix: Compliance Tagging Pipeline"
]

BODIES_EN = [
    "This document details regulatory updates affecting AI deployments across sectors.",
    "The contract introduces audit rights, RBAC policies, and evidence retention rules.",
    "The lawsuit centers on alleged misuse of copyrighted materials during training.",
    "The asset release includes improved redaction and provenance tracking."
]

# Short phrase dictionaries in ko / fr / es / ar / vi to give multilingual flavor
PHRASES = {
    "ko": ["규정", "지침", "계약", "소송", "발표", "업데이트", "감사", "준수"],
    "fr": ["règlementation", "contrat", "procès", "publication", "mise à jour", "conformité"],
    "es": ["regulación", "contrato", "demanda", "publicación", "actualización", "cumplimiento"],
    "ar": ["تنظيم", "عقد", "دعوى", "إصدار", "تحديث", "امتثال"],
    "vi": ["quy định", "hợp đồng", "kiện tụng", "phát hành", "cập nhật", "tuân thủ"]
}

def make_item(i, cat, lang, juris, start_date):
    title_pool = {
        "governance": GOV_TITLES_EN,
        "contract": CONTRACT_TITLES_EN,
        "lawsuit": LAWSUIT_TITLES_EN,
        "asset": ASSET_TITLES_EN
    }[cat]
    title = random.choice(title_pool)
    body = random.choice(BODIES_EN)

    # add multilingual spice
    if lang != "en":
        for _ in range(3):
            body += " " + random.choice(PHRASES.get(lang, []))

    ts = (start_date + timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://example.org/{juris.lower()}/{cat}/{i:05d}"
    ev = [f"Evidence fragment {k} for {cat} item {i}" for k in range(1, 4)]
    return {
        "id": f"GS{i:05d}",
        "title": f"[{juris}] {title}",
        "body": body,
        "category": cat,
        "jurisdiction": juris,
        "language": lang,
        "timestamp": ts,
        "url": url,
        "evidence_spans": ev
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)

    start_date = datetime(2024, 7, 1)
    items = []
    idx = 0

    # Main distribution for en/ko/fr
    for cat, n in CATS:
        for _ in range(n):
            lang = random.choice(LANGS_MAIN)
            juris = random.choice(["EU","US","KR","FR"])
            idx += 1
            items.append(make_item(idx, cat, lang, juris, start_date))

    # Small stress subset for es/ar/vi (approx 10 per lang per cat)
    for cat, _ in CATS:
        for lang in LANGS_STRESS:
            for _ in range(10):
                juris = random.choice(["EU","US","KR","FR"])
                idx += 1
                items.append(make_item(idx, cat, lang, juris, start_date))

    # Shuffle for realism
    random.shuffle(items)

    # Write full jsonl
    with open(outdir / "govsense_1k.jsonl", "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    # Simple split: 70/15/15
    n = len(items)
    n_train = int(0.7 * n); n_dev = int(0.15 * n)
    train = items[:n_train]
    dev = items[n_train:n_train+n_dev]
    test = items[n_train+n_dev:]

    for name, subset in [("train", train), ("dev", dev), ("test", test)]:
        with open(outdir / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for it in subset:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")

    # Label distribution
    from collections import Counter
    cnt = Counter([it["category"] for it in items])
    import csv
    with open(outdir / "labels.csv", "w", newline="", encoding="utf-8") as cf:
        w = csv.writer(cf)
        w.writerow(["label", "count"])
        for k,v in cnt.items():
            w.writerow([k, v])

    print(f"Wrote {len(items)} items to {outdir}")

if __name__ == "__main__":
    main()
