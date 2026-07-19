# Specialist Model Research Spike

## What are we trying to learn?

We want to understand one simple question:

> Is it better for a model to learn a domain by changing its weights, or can a general model do nearly as well when it is given a well-designed external memory and retrieval system?

There are two approaches:

- **Fine-tuning:** teach a general model many examples from one subject. The model changes internally and becomes more specialised.
- **Memory/RAG:** keep the model general, but give it a carefully organised library. Before answering, the system finds useful documents and puts them in the prompt. “RAG” simply means *retrieve useful information, then generate an answer*.

Your job is **not** to build the memory system. Your job is to find a realistic specialist or fine-tuned model that can be used as the comparison point.

## Your task, step by step

### 1. Pick one domain

Choose a subject where specialist knowledge matters. Good examples include:

- checking sustainability or carbon claims;
- verifying energy savings;
- checking green-credit evidence;
- extracting facts from technical documents; or
- another domain with public data and a clear right-or-wrong outcome.

Pick one focused area. Do not try to cover all of sustainability.

### 2. Pick one use case

Describe what a user needs help deciding. For example:

> Given a sustainability claim and its supporting evidence, decide whether the claim is supported.

Write down:

- what goes into the model;
- what the model should return; and
- why the answer matters.

### 3. Choose how to score the answer

This is the **objective function**: the rule used to decide whether an answer is good. Keep it simple and write it down before testing.

For example, if the answer is “supported” or “unsupported,” use:

- **primary metric:** macro F1, which rewards getting both classes right;
- **secondary metric:** accuracy, cost, speed, or evidence quality.

The metric should match the real decision. Do not choose a metric only because it gives a nice-looking score.

### 4. Find and compare candidates

Find at least three plausible combinations of model, data, and task. Check:

- Can the model actually be accessed?
- Is the data public and suitable for testing?
- Is the licence clear?
- Can another person repeat the test?
- Is there a risk that the model has already seen the test answers?

Record this in [`outputs/research_matrix.md`](outputs/research_matrix.md), using [`docs/RESEARCH_MATRIX_TEMPLATE.md`](docs/RESEARCH_MATRIX_TEMPLATE.md).

### 5. Run a small research spike

Test the best candidate on a small sample. You are checking whether the idea works, not building a production benchmark.

Record the model version, data source, sample size, instructions, metric, runtime, errors, and limitations. Follow [`docs/CANDIDATE_TEST_PROTOCOL.md`](docs/CANDIDATE_TEST_PROTOCOL.md).

The included synthetic demo only checks that the repository runs. It is not evidence that a real specialist model works.

### 6. Explain the future comparison

Describe how a later experiment would compare:

1. the specialist or fine-tuned model you tested; and
2. a general model using the proposed memory/RAG architecture.

They should receive the same test questions and be judged with the same metrics. Explain what “close enough” would mean before seeing the final results. Use [`docs/BENCHMARK_DESIGN_TEMPLATE.md`](docs/BENCHMARK_DESIGN_TEMPLATE.md).

## Keep a simple research log

Copy [`docs/ASSUMPTIONS_TEMPLATE.md`](docs/ASSUMPTIONS_TEMPLATE.md) to `outputs/assumptions.md` and record decisions, unknowns, and changes of direction.

Use the team checkpoints in [`docs/WORKING_WITH_US.md`](docs/WORKING_WITH_US.md):

- **kickoff:** what you understood and what you will investigate;
- **direction check:** your chosen domain, use case, candidate, test, and main risk;
- **final risk check:** your conclusion, confidence, and biggest limitation.

## What to deliver

See [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md). The important outputs are:

- a short recommendation;
- a comparison of candidates;
- a small reproducible test;
- machine-readable results;
- a final report; and
- a proposed follow-up comparison.

Use [`report/FINAL_REPORT_TEMPLATE.md`](report/FINAL_REPORT_TEMPLATE.md) for the report structure.

## Setup and checks

Python 3.10+ is required.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
make check
make smoke
```

`make check` runs formatting, linting, and tests. `make smoke` runs the small synthetic example and creates demo files in `outputs/` and `report/`.

Before changing code, read [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md). For the full brief, read [`CHALLENGE.md`](CHALLENGE.md).
## Reproducing the real specialist-model test (ClimateBERT)

The commands above (`make check`, `make smoke`) only exercise the synthetic
rule-based demo baked into this repository. They prove the pipeline runs; they
are not evidence about a real specialist model.

The actual specialist-model spike test used in this submission is in
`src/benchmark_challenge/run_climate_test.py`. It:

- loads `amandakonet/climatebert-fact-checking` (ClimateBERT fine-tuned for
  claim/evidence verification) from Hugging Face;
- samples claim/evidence pairs from `amandakonet/climate_fever_adopted`;
- runs inference and computes the same `classification_metrics` used elsewhere
  in this repository;
- writes results to `outputs/results.csv`.

### Option A: Run locally

```bash
python -m pip install -e '.[dev]'
python -m pip install torch transformers datasets
python -m benchmark_challenge.run_climate_test --sample-size 30 --seed 42 --output outputs/results.csv
```

### Option B: Run in Docker (recommended for a clean, reproducible environment)

```bash
docker build -t ds-intern-challenge .
docker run --rm -v "$(pwd)/outputs:/app/outputs" -v "$(pwd)/report:/app/report" ds-intern-challenge
```

This builds an image with the base package plus `torch`, `transformers`, and
`datasets`, runs the full check + smoke + real specialist test, and writes
`outputs/results.csv` back to your local `outputs/` folder via the volume mount.

### Option C: Run in Google Colab

A Colab-based walkthrough (with intermediate outputs and label-mapping checks)
is documented step by step in `outputs/assumptions.md` and `report/final_report.md`.

### Known limitations of this test

- Sample size is small (default 30 rows) by design — see `outputs/assumptions.md`
  for why this is a feasibility spike, not a statistically validated benchmark.
- There is a documented train/test contamination risk, since the evaluation
  dataset is closely related to the model's original fine-tuning data — see
  `outputs/research_matrix.md`.
- Model licence terms are not explicitly stated on the model card; confirm
  before any production use.


