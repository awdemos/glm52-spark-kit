"""CPU-only unit tests for benchmarks/correctness_probe.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "benchmarks"))
import correctness_probe as correctness_probe


def test_degenerate_truncated_text():
    assert correctness_probe.degenerate("hi") is None


def test_degenerate_unique_word_ratio_low():
    text = "foo " * 50
    reason = correctness_probe.degenerate(text)
    assert reason is not None
    assert "unique-word ratio" in reason


def test_degenerate_repetition_loop_short_cycle():
    text = " ".join(["alpha beta"] * 6)
    reason = correctness_probe.degenerate(text)
    assert reason is not None
    assert "cycle" in reason


def test_degenerate_dominant_token():
    words = ["foo"] * 20 + ["bar", "baz", "qux", "quux", "quuux",
                           "one", "two", "three", "four", "five"]
    reason = correctness_probe.degenerate(" ".join(words))
    assert reason is not None
    assert "foo" in reason


def test_degenerate_healthy_text():
    text = " ".join(f"word{i}" for i in range(100))
    assert correctness_probe.degenerate(text) is None
