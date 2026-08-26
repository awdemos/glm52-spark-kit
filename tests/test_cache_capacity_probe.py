"""CPU-only unit tests for benchmarks/cache_capacity_probe.py."""
import sys
from pathlib import Path

# The module parses sys.argv at import time; give it a clean argv for import.
_orig_argv = sys.argv[:]
sys.argv = ["cache_capacity_probe.py"]
sys.path.insert(0, str(Path(__file__).parent.parent / "benchmarks"))
import cache_capacity_probe as cache_capacity_probe

sys.argv = _orig_argv


def test_prefix_for_contains_conversation_id():
    p0 = cache_capacity_probe.prefix_for(0)
    assert p0.startswith("[conversation 0 key ")
    nonce = p0.split("[conversation 0 key ", 1)[1].split("]", 1)[0]
    assert len(nonce) == 8
    assert nonce.isalpha() and nonce.islower()


def test_prefix_for_is_distinct_between_conversations():
    p0 = cache_capacity_probe.prefix_for(0)
    p1 = cache_capacity_probe.prefix_for(1)
    assert p0 != p1
    assert "[conversation 0 key" in p0
    assert "[conversation 1 key" in p1


def test_prefix_for_contains_repeated_unit():
    prefix = cache_capacity_probe.prefix_for(0)
    assert cache_capacity_probe.UNIT in prefix
    assert prefix.count(cache_capacity_probe.UNIT) == cache_capacity_probe.REPS
