"""
Runs the ClimateBERT fact-checking specialist model on a small sample of
climate claim/evidence pairs and computes classification metrics.

This is the real specialist-model test referenced in outputs/research_matrix.md,
outputs/recommendation.md, and report/final_report.md. It is separate from the
synthetic smoke test in run_demo.py, which only proves the repository plumbing works.

Usage:
    python -m benchmark_challenge.run_climate_test --sample-size 30 --seed 42 \
        --output outputs/results.csv

Requires (not part of the base package, install separately):
    pip install torch transformers datasets

This script downloads a public Hugging Face model and dataset on first run.
No credentials, private data, or proprietary material are used.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd

from .metrics import classification_metrics

MODEL_NAME = "amandakonet/climatebert-fact-checking"
DATASET_NAME = "amandakonet/climate_fever_adopted"

LABEL_ALIGN = {
    "LABEL_0": "SUPPORTS",
    "LABEL_1": "REFUTES",
    "LABEL_2": "NOT_ENOUGH_INFO",
}


def build_sample(sample_size: int, seed: int) -> pd.DataFrame:
    from datasets import load_dataset

    ds = load_dataset(DATASET_NAME, split="test")
    frame = pd.DataFrame(ds).sample(sample_size, random_state=seed).reset_index(drop=True)
    return frame


def run_inference(frame: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()

    preds = []
    start = time.time()
    for _, row in frame.iterrows():
        inputs = tokenizer(row["claim"], row["evidence"], return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        pred_id = logits.argmax(-1).item()
        preds.append(model.config.id2label[pred_id])
    runtime_seconds = time.time() - start

    frame["predicted_label_raw"] = preds
    frame["predicted_label"] = frame["predicted_label_raw"].map(LABEL_ALIGN)
    return frame, runtime_seconds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="outputs/results.csv")
    args = parser.parse_args()

    frame = build_sample(args.sample_size, args.seed)
    frame, runtime_seconds = run_inference(frame)

    metrics = classification_metrics(frame["evidence_label"], frame["predicted_label"])
    for name, value in metrics.items():
        frame[name] = value
    frame["model_name"] = MODEL_NAME
    frame["dataset_name"] = DATASET_NAME
    frame["runtime_seconds"] = runtime_seconds
    frame["sample_size"] = len(frame)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)

    print(
        {
            "rows": len(frame),
            **metrics,
            "runtime_seconds": runtime_seconds,
            "output": str(output),
        }
    )


if __name__ == "__main__":
    main()
