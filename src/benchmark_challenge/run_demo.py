from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .metrics import classification_metrics


def simple_rule(text: str) -> str:
    """Synthetic smoke-test baseline; replace this with the selected model."""
    evidence_terms = ("metered", "bills", "audit", "third-party", "verified")
    return "supported" if any(term in text.lower() for term in evidence_terms) else "unsupported"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    required = {"id", "text", "label"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    frame["prediction"] = frame["text"].map(simple_rule)
    metrics = classification_metrics(frame["label"], frame["prediction"])
    for name, value in metrics.items():
        frame[name] = value

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    print({"rows": len(frame), **metrics, "output": str(output)})


if __name__ == "__main__":
    main()
