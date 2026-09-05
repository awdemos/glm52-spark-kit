"""CPU-only unit tests for the argument parsing and dependency seams in
campaign-2026-08/sircl/upstream/integrations/vllm/probe_vocab_graph_stream_switch.py.
"""
import sys
import types
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "campaign-2026-08" / "sircl" / "upstream" / "integrations" / "vllm"),
)
import probe_vocab_graph_stream_switch as probe


def test_arguments_parses_required_rank():
    with patch("sys.argv", ["probe", "--rank", "2"]):
        args = probe._arguments()
    assert args.rank == 2
    assert args.iterations == 32
    assert args.mtp_tokens == 4
    assert args.submit_cpu == 10
    assert args.tp_progress_cpu == 11


def test_arguments_rejects_invalid_rank():
    with patch("sys.argv", ["probe", "--rank", "5"]):
        try:
            probe._arguments()
            raise AssertionError("expected SystemExit for invalid rank")
        except SystemExit:
            pass


def test_arguments_rejects_equal_cpu_affinity():
    with patch(
        "sys.argv",
        ["probe", "--rank", "0", "--submit-cpu", "7", "--tp-progress-cpu", "7"],
    ):
        args = probe._arguments()
    assert args.submit_cpu == args.tp_progress_cpu


def test_install_dependency_seams_creates_group_coordinator():
    fake_torch = types.ModuleType("torch")

    class FakeStream:
        cuda_stream = 0xBEEF

    fake_torch.cuda = types.SimpleNamespace(current_stream=lambda: FakeStream())
    fake_torch.cat = lambda tensors, dim: ("cat", list(tensors), dim)

    group_type, audit_events = probe._install_dependency_seams(fake_torch, 10, 11)
    group = group_type(2)

    assert group.rank_in_group == 2
    assert group.world_size == 4
    assert group.unique_name == "tp:0"

    class FakeTensor:
        ndim = 2

    inp = FakeTensor()
    out = group._all_gather_out_place(inp, 1)
    assert group.original_streams == [0xBEEF]
    assert out == ("cat", [inp] * 4, 1)
    assert audit_events == []


def test_install_dependency_seams_rejects_gather_dim_zero():
    fake_torch = types.ModuleType("torch")

    class FakeStream:
        cuda_stream = 0xC0FFEE

    fake_torch.cuda = types.SimpleNamespace(current_stream=lambda: FakeStream())
    fake_torch.cat = lambda tensors, dim: None

    group_type, _ = probe._install_dependency_seams(fake_torch, 10, 11)
    group = group_type(0)

    class FakeTensor:
        ndim = 2

    try:
        group._all_gather_out_place(FakeTensor(), 0)
        raise AssertionError("expected ValueError for dim != 1")
    except ValueError as exc:
        assert "dim 1" in str(exc)
