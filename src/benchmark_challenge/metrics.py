from __future__ import annotations

from collections.abc import Iterable

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def classification_metrics(y_true: Iterable[str], y_pred: Iterable[str]) -> dict[str, float]:
    true = list(y_true)
    pred = list(y_pred)
    return {
        "accuracy": float(accuracy_score(true, pred)),
        "macro_f1": float(f1_score(true, pred, average="macro", zero_division=0)),
        "macro_precision": float(precision_score(true, pred, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(true, pred, average="macro", zero_division=0)),
    }
