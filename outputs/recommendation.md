# Recommendation

## Short recommendation

`amandakonet/climatebert-fact-checking` is a credible, publicly accessible specialist baseline for a
future comparison against a general model + RAG architecture on climate/sustainability claim
verification. It is directly accessible, task-matched, and technically workable, but this spike's
results should be treated as a feasibility signal, not a validated performance benchmark.

## Confidence level: LOW-to-MODERATE

Confidence is limited by three factors: (1) a 30-row sample size, (2) a heavily imbalanced class
distribution (20 NOT_ENOUGH_INFO, 8 SUPPORTS, 2 REFUTES), and (3) a likely train/test overlap between
the model's original fine-tuning data and our test sample. All three inflate uncertainty around the
reported macro F1 of 0.41.

## What we found

- **Setup works end-to-end:** model loads, accepts claim+evidence pairs, and returns valid predictions
  in about 10.8 seconds for 30 rows (~0.36s/row) on a standard Colab CPU runtime.
- **Accuracy (0.70) overstates real performance** relative to macro F1 (0.41), because of class imbalance.
  This confirms macro F1 was the correct primary metric choice.
- **Dominant error pattern:** the model over-predicted SUPPORTS in ambiguous or loosely related
  claim-evidence pairs (7 of 9 errors), including one case where it inverted a REFUTES case into
  SUPPORTS — the most costly kind of mistake for a claim-verification tool.

## What this does NOT establish

- Whether the model generalizes to genuinely unseen claims (contamination risk not resolved).
- Whether the model outperforms or underperforms a general model + RAG system — that comparison was
  not run in this repository, by design.
- A statistically reliable performance number — 30 rows is too small for that, and this was intentional
  scope, not an oversight.

## Recommended next step

Before using this model as the official specialist baseline in the future benchmark:

1. Source or construct a held-out test set with no overlap with `climate_fever_adopted`.
2. Re-run on at least 100-200 balanced rows to get a stable macro F1 estimate.
3. Confirm licensing terms for the model before any commercial use.
4. Proceed to the future benchmark design (see `benchmark_design.md`) once the above is resolved.
