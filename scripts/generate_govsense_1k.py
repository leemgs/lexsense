import argparse, subprocess, sys, os
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output directory, e.g., data/govsense_1k")
    args = ap.parse_args()
    out = Path(args.out)
    cmd = [sys.executable, "-m", "lexsense.ingest.generator_govsense", "--out", str(out)]
    raise SystemExit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
