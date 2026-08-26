"""CPU-only tests for apply.sh and verify.sh argument handling.

Both scripts are exercised by copying them into a temporary directory with a
minimal MANIFEST.json, then invoking them as subprocesses. This keeps the tests
free of vLLM, CUDA, and ssh dependencies.
"""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


REPO = Path(__file__).parent.parent


def _copy_script(tmp: Path, name: str) -> Path:
    dst = tmp / name
    dst.write_text((REPO / name).read_text())
    dst.chmod(0o755)
    return dst


def _make_manifest(tmp: Path, entries):
    manifest = {
        "site_packages_root": "/usr/local/lib/python3.12/dist-packages",
        "base_image": "test",
        "files": entries,
    }
    (tmp / "MANIFEST.json").write_text(json.dumps(manifest))


def test_apply_sh_emits_mount_for_core_set():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        apply = _copy_script(tmp, "apply.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        (overlay / "vllm").mkdir(parents=True)
        (overlay / "vllm" / "dummy.py").write_text("print('hello')")
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/dummy.py",
                "site_packages_target": "vllm/dummy.py",
                "md5": "dummy",
                "sets": ["core"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(apply), "core", str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert '-v' in result.stdout
        assert str(overlay / "vllm/dummy.py") in result.stdout


def test_apply_sh_omits_non_core_set():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        apply = _copy_script(tmp, "apply.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        (overlay / "vllm").mkdir(parents=True)
        (overlay / "vllm" / "dummy.py").write_text("print('hello')")
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/dummy.py",
                "site_packages_target": "vllm/dummy.py",
                "md5": "dummy",
                "sets": ["adaptive"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(apply), "core", str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""


def test_apply_sh_all_set_includes_every_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        apply = _copy_script(tmp, "apply.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        (overlay / "vllm").mkdir(parents=True)
        (overlay / "vllm" / "dummy.py").write_text("print('hello')")
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/dummy.py",
                "site_packages_target": "vllm/dummy.py",
                "md5": "dummy",
                "sets": ["adaptive"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(apply), "all", str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "vllm/dummy.py" in result.stdout


def test_apply_sh_fails_on_missing_overlay_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        apply = _copy_script(tmp, "apply.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/missing.py",
                "site_packages_target": "vllm/missing.py",
                "md5": "dummy",
                "sets": ["core"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(apply), "core", str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "missing" in (result.stdout + result.stderr)


def test_verify_sh_passes_for_valid_overlay():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        verify = _copy_script(tmp, "verify.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        (overlay / "vllm").mkdir(parents=True)
        content = b"print('hello')"
        (overlay / "vllm" / "dummy.py").write_bytes(content)
        md5 = hashlib.md5(content).hexdigest()
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/dummy.py",
                "site_packages_target": "vllm/dummy.py",
                "md5": md5,
                "sets": ["core"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(verify), str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "OK" in result.stdout


def test_verify_sh_fails_on_md5_mismatch():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        verify = _copy_script(tmp, "verify.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        (overlay / "vllm").mkdir(parents=True)
        (overlay / "vllm" / "dummy.py").write_text("print('hello')")
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/dummy.py",
                "site_packages_target": "vllm/dummy.py",
                "md5": "00000000000000000000000000000000",
                "sets": ["core"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(verify), str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "MISMATCH" in result.stdout


def test_verify_sh_fails_on_missing_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        verify = _copy_script(tmp, "verify.sh")
        overlay = tmp / "overlays"
        overlay.mkdir()
        _make_manifest(tmp, [
            {
                "overlay_file": "vllm/missing.py",
                "site_packages_target": "vllm/missing.py",
                "md5": "00000000000000000000000000000000",
                "sets": ["core"],
                "provenance": "test",
            }
        ])
        result = subprocess.run(
            [str(verify), str(overlay)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "MISMATCH" in result.stdout
