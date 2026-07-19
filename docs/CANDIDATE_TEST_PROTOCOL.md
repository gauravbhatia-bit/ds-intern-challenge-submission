# Candidate Test Protocol

Use this protocol for every specialist or fine-tuned model candidate. It defines the minimum evidence required before recommending a baseline.

## Test record

- **Use case and decision:** What real sustainability or adjacent domain decision does this support?
- **Input:** What does the model receive?
- **Expected output:** What label, extraction, ranking, verification, or forecast is required?
- **Hypothesis:** What should this candidate demonstrate?
- **Model:** Exact identifier, version/checkpoint, access method, and license.
- **Data:** Source, version/date, license, provenance, split, and contamination risk.
- **Sample:** Number of examples and selection rule.
- **Objective:** Exact scoring function and direction of improvement.
- **Metrics:** Primary metric and at least one secondary metric.
- **Controls:** Prompt, parameters, seed, hardware/API environment, and repeated-run policy.
- **Result:** Machine-readable result plus representative successes and failures.
- **Limitations:** What this test cannot establish.

## Acceptance rule

A candidate is feasible only when another contributor can reproduce the test from the recorded setup and the result informs the proposed comparison against a general model using external memory and retrieval. A repository smoke test, model import, or generic unit test alone is not candidate evidence.
