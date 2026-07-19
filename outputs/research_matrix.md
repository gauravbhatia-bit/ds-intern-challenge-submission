# Research Matrix

## Candidate 1 — SELECTED: ClimateBERT Fact-Checking (Verification Task)

- **Model:** `amandakonet/climatebert-fact-checking` (ClimateBERT fine-tuned on textual entailment using Climate FEVER data)
- **Dataset:** `amandakonet/climate_fever_adopted` (Hugging Face, same source used to fine-tune the model)
- **Task type:** 3-class classification (SUPPORTS / REFUTES / NOT_ENOUGH_INFO)
- **Accessible?** Yes — public Hugging Face model, loads via `transformers.AutoModelForSequenceClassification`, no gating or API key required.
- **Data public and suitable?** Yes — public dataset, pre-formatted as claim/evidence/label triples.
- **Licence clear?** Model card does not state an explicit licence; underlying Climate FEVER dataset is released for research use. Flagged as an open question — needs clarification before any production use.
- **Reproducible by another person?** Yes — deterministic given fixed random seed, model version, and dataset version recorded below.
- **Train/test contamination risk?** HIGH. The evaluation dataset (`climate_fever_adopted`) is very likely the same data (or a close split of it) used to fine-tune this model. This means our F1 score reflects in-domain performance, not generalization to unseen claims. This is the primary caveat of this spike.
- **Why selected:** Only candidate with a model specifically fine-tuned for the exact verification task (claim + evidence to a label), publicly accessible, and quick to test within scope.

## Candidate 2 — REJECTED: ClimateBERT Environmental Claims (Detection Task)

- **Model:** `climatebert/environmental-claims`
- **Dataset:** `climatebert/environmental_claims` (Hugging Face)
- **Task type:** Binary classification (claim / not a claim)
- **Accessible?** Yes, public.
- **Data public and suitable?** Yes, but answers a different question.
- **Licence clear?** Apache 2.0 license family typical of ClimateBERT releases.
- **Reproducible?** Yes.
- **Contamination risk?** Unknown, not tested.
- **Why rejected:** This model detects *whether* a sentence makes an environmental claim, not *whether the claim is supported by evidence*. It does not match our use case (claim verification against evidence), so it was not carried forward into the technical test.

## Candidate 3 — REJECTED (for now): General LLM Zero-Shot Baseline

- **Model:** Any general-purpose LLM (e.g., open Llama/Mistral or GPT-family via API) prompted zero-shot with claim + evidence.
- **Dataset:** Same `climate_fever_adopted` sample, for a fair future comparison.
- **Task type:** Same 3-class classification, framed as a prompting task.
- **Accessible?** Yes, in principle (open models locally, or API-based models with a key).
- **Data public and suitable?** Yes, same dataset as Candidate 1.
- **Licence clear?** Depends on chosen model; needs to be confirmed at implementation time.
- **Reproducible?** Only if prompt, model version, and temperature/sampling settings are fixed and logged.
- **Contamination risk?** Lower than Candidate 1, since the LLM was not deliberately fine-tuned on this dataset (though large pretraining corpora may still include some overlapping text).
- **Why not tested in this spike:** Explicitly out of scope per CHALLENGE.md — this repository is not meant to build the RAG/general-model comparison side. It is documented here for completeness and for the future benchmark design.

## Summary comparison

| Candidate | Task match | Accessible | Data public | Licence clear | Contamination risk | Selected? |
|---|---|---|---|---|---|---|
| ClimateBERT fact-checking | Exact match | Yes | Yes | Unclear | High | Yes |
| ClimateBERT environmental-claims | Wrong task | Yes | Yes | Yes (Apache 2.0) | Untested | No |
| General LLM zero-shot | Exact match | Yes | Yes | Model-dependent | Lower | Deferred to future benchmark |
