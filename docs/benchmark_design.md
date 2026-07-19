# Benchmark Design: Fine-Tuned Specialist vs General Model + RAG

## Purpose

This document proposes how a future experiment should fairly compare our tested specialist baseline
(ClimateBERT fact-checking) against a general-purpose model supported by an external memory/RAG
architecture. This repository does not build or run that RAG system; it only defines the comparison.

## What each side receives

Both systems must receive the exact same inputs and be judged by the exact same rules.

- **Shared test set:** A held-out sample of claim + evidence pairs from a climate/sustainability claim
  dataset, ideally NOT drawn from `climate_fever_adopted` (to avoid the contamination risk already
  flagged for the specialist model), or at minimum a split that excludes rows used in the specialist
  model's fine-tuning.
- **Same question format:** "Given this claim and this evidence, is the claim SUPPORTED, REFUTED, or
  is there NOT ENOUGH INFO?"
- **Same output format:** A single label from the same three-class set, so predictions are directly
  comparable without post-hoc normalization differences.

## The two systems being compared

| System | What it is | What it receives |
|---|---|---|
| Specialist baseline | ClimateBERT fact-checking (tested in this repo) | Claim + evidence, directly |
| General model + RAG | A general LLM with a retrieval layer over a claim-evidence corpus | Claim, evidence retrieved by the RAG system (not hand-fed) |

Note the key structural difference: the specialist model is given evidence directly, while the RAG
system must first retrieve relevant evidence itself. The benchmark must record retrieval quality
separately from final answer quality, since a wrong verdict caused by bad retrieval is a different
failure mode than a wrong verdict caused by bad reasoning over correct evidence.

## Metrics (must match across both systems)

- **Primary metric:** Macro F1 across SUPPORTS / REFUTES / NOT_ENOUGH_INFO — same as used in this spike.
- **Secondary metrics:**
  - Accuracy (for context, not primary decision-making)
  - Latency per query (specialist inference time vs. RAG retrieval + generation time)
  - Cost per query (compute cost for local model vs. API/token cost for LLM + retrieval)
  - Evidence quality (for RAG only: did it retrieve the correct supporting evidence, measured separately
    from the final label accuracy)

## Fairness controls

- **Same test data, same order, same random seed** for any sampling.
- **Version pinning:** record exact model checkpoint hashes, RAG embedding model version, and retrieval
  corpus snapshot date, so the test is reproducible.
- **Repeated runs:** run each system at least 3 times on the same test set to check for variance
  (especially important for the general LLM, which may have non-deterministic outputs).
- **No prompt hand-tuning advantage:** the RAG prompt and the specialist model's input format should each
  be finalized before seeing results, not iteratively tuned against the test set.
- **Blind scoring:** whoever grades ambiguous cases should not know which system produced which answer.

## Defining "close enough" in advance

Before running the future benchmark, we propose the following threshold, decided now rather than after
seeing results:

> The general model + RAG approach will be considered "approaching specialist performance" if its macro F1
> is within 5 percentage points of the specialist baseline's macro F1 on the same shared test set, AND its
> per-query latency and cost are documented (even if higher), so a real trade-off decision can be made.

If RAG scores lower but is dramatically cheaper/faster, or if RAG scores higher because the specialist's
fine-tuning data is stale, both outcomes should be reported as decision-relevant findings rather than a
simple pass/fail on the 5-point threshold alone.

## Why this comparison is useful, not just convenient

- Fine-tuning requires retraining whenever the domain evidence base changes (e.g., new sustainability
  regulations or claims); RAG only requires updating the retrieval corpus. This affects real maintenance cost.
- If RAG performs close to the specialist model, it argues for a cheaper, more maintainable production
  architecture. If the specialist clearly wins, it justifies the retraining investment.
- Testing both on identical inputs, with identical scoring, removes the risk of an apples-to-oranges
  comparison that would make the business decision unreliable.

## What this future benchmark would need that this repository does not build

- A retrieval corpus and embedding/index pipeline (explicitly out of scope for this repository).
- A larger, contamination-checked test set (target: hundreds of rows, not 30).
- Infrastructure to run and time both systems under comparable conditions.
