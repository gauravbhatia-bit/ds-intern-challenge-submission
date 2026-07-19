from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    frame = pd.read_csv(args.results)
    metric_names = ["accuracy", "macro_f1", "macro_precision", "macro_recall"]
    metrics = {name: float(frame[name].iloc[0]) for name in metric_names}

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image_path = output.with_name("demo_metric.png")

    plt.figure(figsize=(8, 4.5))
    plt.bar(metrics.keys(), metrics.values())
    plt.ylim(0, 1)
    plt.ylabel("Score")
    plt.title("Synthetic smoke-test metrics — replace with real experiment")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(image_path, dpi=160)
    plt.close()

    errors = frame.loc[frame["label"] != frame["prediction"], ["id", "text", "label", "prediction"]]
    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Benchmark Smoke Test</title>
<style>
body{{font-family:Arial,sans-serif;max-width:960px;margin:40px auto;line-height:1.5}}
table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}}
.note{{padding:14px;background:#fff4ce}}
</style></head>
<body>
<h1>Benchmark Smoke Test</h1>
<p class='note'><strong>Demonstration only.</strong> This synthetic rule-based baseline exists to
prove the repository workflow. Replace it with a real selected model, dataset, and evaluation.</p>
<h2>Metrics</h2><img src='{image_path.name}' style='max-width:100%'>
<h2>Error analysis</h2>{errors.to_html(index=False, escape=True)}
<h2>Required interpretation</h2><p>Explain what the metric means, what it does not establish,
and whether the test supports proceeding to a full benchmark.</p>
</body></html>"""
    output.write_text(html, encoding="utf-8")
    print({"report": str(output), "chart": str(image_path)})


if __name__ == "__main__":
    main()
