# Reproducibility environment for the ClimateBERT specialist model test.
# Base package (pandas, sklearn, matplotlib, pytest, ruff) comes from pyproject.toml.
# torch/transformers/datasets are added here since they are only needed for the
# real specialist-model test, not for the base repository's tests/demo.

FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY data ./data
COPY docs ./docs

RUN pip install --upgrade pip && \
    pip install -e ".[dev]" && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install transformers datasets

RUN mkdir -p outputs report

# Default: run the base test suite + synthetic smoke demo to prove the repo works.
CMD ["sh", "-c", "ruff check src tests && pytest -q && python -m benchmark_challenge.run_demo --input data/synthetic_claims.csv --output outputs/demo_results.csv && python -m benchmark_challenge.run_climate_test --output outputs/results.csv"]
