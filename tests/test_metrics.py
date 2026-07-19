from benchmark_challenge.metrics import classification_metrics
from benchmark_challenge.run_demo import simple_rule


def test_perfect_predictions() -> None:
    result = classification_metrics(["a", "b"], ["a", "b"])
    assert result["accuracy"] == 1.0
    assert result["macro_f1"] == 1.0


def test_classification_metrics_handles_missed_class_without_warning() -> None:
    result = classification_metrics(["supported", "unsupported"], ["supported", "supported"])
    assert result["accuracy"] == 0.5
    assert result["macro_f1"] == 1 / 3


def test_simple_rule_is_case_insensitive_and_conservative() -> None:
    assert simple_rule("A THIRD-PARTY report is verified.") == "supported"
    assert simple_rule("The project is better for the planet.") == "unsupported"
