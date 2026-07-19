# Assumptions and Research Log

## Domain and use case decisions

- **Chosen domain:** Sustainability / climate claim verification, selected over energy-savings and green-credit verification because it has the richest public labeled datasets and the clearest binary/ternary ground truth.
- **Chosen use case:** Given a claim and a supporting evidence sentence, classify the relationship as SUPPORTS, REFUTES, or NOT_ENOUGH_INFO.
- **Why this matters:** Automated claim verification is directly relevant to greenwashing detection and ESG compliance, a real commercial decision-support need.

## Metric decisions

- **Primary metric:** Macro F1 — chosen because the label classes are imbalanced in real-world data (NOT_ENOUGH_INFO dominates), and macro F1 avoids rewarding a model that just predicts the majority class.
- **Secondary metrics:** Accuracy, macro precision, macro recall, and runtime.
- **Observed gap:** Accuracy (0.70) was substantially higher than macro F1 (0.41) on our sample, confirming the metric choice was correct — accuracy alone would have overstated performance.

## Sample size decision

- Used 30 claim-evidence rows sampled from `amandakonet/climate_fever_adopted` (test split), fixed random seed for reproducibility.
- **Explicit limitation:** 30 rows is a feasibility spike, not a statistically reliable benchmark. Class distribution was heavily skewed (20 NOT_ENOUGH_INFO, 8 SUPPORTS, 2 REFUTES), meaning the REFUTES F1 score is highly sensitive to a single misclassification.
- This sample size and imbalance mean the reported macro F1 (0.41) should not be treated as the model's "true" performance — only as evidence the pipeline and model are technically workable.

## Dataset substitution

- Originally attempted to load the legacy `climate_fever` dataset via Hugging Face `datasets` library; this failed with an `HfUriError` because the library version installed in Colab requires a `namespace/name` format and no longer resolves legacy canonical dataset names.
- Switched to `amandakonet/climate_fever_adopted`, which is correctly namespaced and is the same dataset used to originally fine-tune our selected model.
- **Consequence flagged as a risk:** because the model was fine-tuned on this same dataset (or a close variant of it), our test may partially measure memorized/in-domain performance rather than generalization to unseen claims. This is recorded as a contamination risk in `research_matrix.md`.

## Model behavior observations

- Contrary to our initial hypothesis (that the model would default to NOT_ENOUGH_INFO as a "safe" prediction under uncertainty), error analysis showed the opposite: 7 of 9 errors were the model over-predicting SUPPORTS for claims that were actually NOT_ENOUGH_INFO or REFUTES.
- Most concerning single error: one REFUTES case was predicted as SUPPORTS, which is the costliest type of mistake for a claim-verification tool (inverting the ground truth rather than being merely uncertain).
- This is a qualitative finding from a 30-row sample and should be treated as a hypothesis for further testing, not a confirmed model weakness.

## Open questions / unresolved

- Licence terms for `amandakonet/climatebert-fact-checking` are not explicitly stated on the model card; needs clarification before any production use.
- Unknown how much train/test overlap exists between the model's original fine-tuning data and our 30-row sample; a held-out or newer claims dataset would be needed to properly test generalization.
- The general LLM zero-shot / RAG comparison side was not run in this repository, per challenge scope boundaries; it is deferred to the future benchmark design.

## Changes of direction

- Started with `climate_fever` (original dataset name) -> blocked by library compatibility -> switched to `amandakonet/climate_fever_adopted`.
- Initially assumed model outputs would be human-readable labels; discovered they are generic `LABEL_0/1/2`, requiring manual mapping based on the model card's documented `['entailment', 'contradiction', 'neutral']` order.
