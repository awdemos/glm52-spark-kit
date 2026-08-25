"""CPU-only unit tests for campaign-2026-08/tailquant/split.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "campaign-2026-08" / "tailquant"))
import split as tailquant_split


def test_gini_uniform_distribution():
    assert abs(tailquant_split.gini([10, 10, 10, 10]) - 0.0) < 1e-9


def test_gini_perfectly_unequal():
    assert abs(tailquant_split.gini([0, 0, 0, 100]) - 0.75) < 1e-9


def test_gini_empty_total_returns_zero():
    assert tailquant_split.gini([0, 0, 0, 0]) == 0.0


def test_split_layer_hits_coverage_target():
    counts = [50, 30, 10, 5, 3, 2]
    hot, cold, cov = tailquant_split.split_layer(
        counts, target_coverage=0.8, min_hot=1, max_hot=5
    )
    assert hot == [0, 1]
    assert cold == [2, 3, 4, 5]
    assert abs(cov - 0.8) < 1e-9


def test_split_layer_respects_min_hot():
    counts = [100, 1, 1, 1, 1]
    hot, cold, cov = tailquant_split.split_layer(
        counts, target_coverage=0.5, min_hot=2, max_hot=5
    )
    assert len(hot) >= 2
    assert cov >= 0.5
    assert set(hot) | set(cold) == set(range(len(counts)))


def test_split_layer_respects_max_hot():
    counts = [100, 90, 80, 70, 60, 50]
    hot, cold, cov = tailquant_split.split_layer(
        counts, target_coverage=0.99, min_hot=1, max_hot=3
    )
    assert len(hot) == 3
    assert set(hot) | set(cold) == set(range(len(counts)))


def test_split_layer_empty_counts_falls_back_to_min_hot():
    hot, cold, cov = tailquant_split.split_layer(
        [0, 0, 0, 0], target_coverage=0.9, min_hot=2, max_hot=4
    )
    assert hot == [0, 1]
    assert cov == 0.0
