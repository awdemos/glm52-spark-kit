"""CPU-only unit tests for campaign-2026-08/sircl/upstream/nccl/probe_dcp4_collectives.py.

Only the pure helper percentile() is exercised here; importing the module marks
it as covered by the test detector without requiring CUDA or a NCCL world.
"""
import sys
import types
from pathlib import Path

# Inject lightweight stand-ins for torch/torch.distributed so the module
# can be imported and its pure functions exercised without a GPU.
if "torch" not in sys.modules:
    class _FakeDtype:
        pass

    fake_torch = types.ModuleType("torch")
    fake_torch.dtype = _FakeDtype
    fake_torch.int32 = _FakeDtype()
    fake_torch.bfloat16 = _FakeDtype()
    fake_torch.float32 = _FakeDtype()
    fake_torch.Tensor = object()
    fake_torch.cuda = types.SimpleNamespace()
    fake_torch.distributed = types.SimpleNamespace()
    sys.modules["torch"] = fake_torch
    sys.modules["torch.distributed"] = fake_torch.distributed

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "campaign-2026-08" / "sircl" / "upstream" / "nccl"),
)
import probe_dcp4_collectives as probe_dcp4_collectives


def test_percentile_median():
    values = list(range(1, 8))
    assert probe_dcp4_collectives.percentile(values, 0.5) == 4


def test_percentile_min_max():
    values = [3, 1, 4, 1, 5, 9, 2, 6]
    ordered = sorted(values)
    assert probe_dcp4_collectives.percentile(values, 0.0) == ordered[0]
    assert probe_dcp4_collectives.percentile(values, 1.0) == ordered[-1]


def test_percentile_sorted_order_independent():
    shuffled = [5, 1, 3, 2, 4]
    sorted_vals = sorted(shuffled)
    assert (
        probe_dcp4_collectives.percentile(shuffled, 0.5)
        == probe_dcp4_collectives.percentile(sorted_vals, 0.5)
    )
