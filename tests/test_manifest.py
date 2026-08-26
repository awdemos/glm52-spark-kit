"""CPU-only validation tests for MANIFEST.json."""
import json
from pathlib import Path


REPO = Path(__file__).parent.parent


def _manifest():
    return json.loads((REPO / "MANIFEST.json").read_text())


def test_manifest_is_valid_json():
    manifest = _manifest()
    assert isinstance(manifest, dict)
    assert "site_packages_root" in manifest
    assert "files" in manifest
    assert len(manifest["files"]) > 0


def test_manifest_entries_have_required_fields():
    manifest = _manifest()
    required = {"overlay_file", "site_packages_target", "md5", "sets", "provenance"}
    for entry in manifest["files"]:
        assert required <= set(entry.keys())
        assert isinstance(entry["sets"], list)
        assert len(entry["md5"]) == 32


def test_manifest_sets_are_known():
    manifest = _manifest()
    known = {"core", "indexer", "adaptive", "all"}
    for entry in manifest["files"]:
        for s in entry["sets"]:
            assert s in known, f"unknown set {s!r} in {entry['overlay_file']}"


def test_manifest_site_packages_targets_unique():
    manifest = _manifest()
    targets = [f["site_packages_target"] for f in manifest["files"]]
    assert len(targets) == len(set(targets))


def test_manifest_overlay_files_exist():
    manifest = _manifest()
    overlay_root = REPO / "overlays"
    for entry in manifest["files"]:
        path = overlay_root / entry["overlay_file"]
        assert path.exists(), f"missing overlay file: {entry['overlay_file']}"


def test_manifest_md5s_are_valid_hex():
    manifest = _manifest()
    for entry in manifest["files"]:
        assert len(entry["md5"]) == 32
        # Confirm it is a valid hexadecimal string.
        int(entry["md5"], 16)


def test_manifest_sets_are_nonempty():
    manifest = _manifest()
    for entry in manifest["files"]:
        assert entry["sets"]
        assert isinstance(entry["sets"], list)
