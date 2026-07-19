.PHONY: check format-check lint smoke test run report clean

check: format-check lint test

format-check:
	ruff format --check src tests

lint:
	ruff check src tests

smoke: test run report

test:
	pytest -q

run:
	python -m benchmark_challenge.run_demo --input data/synthetic_claims.csv --output outputs/demo_results.csv

report:
	python -m benchmark_challenge.make_report --results outputs/demo_results.csv --output report/demo_report.html

clean:
	rm -f outputs/demo_results.csv report/demo_report.html report/demo_metric.png
