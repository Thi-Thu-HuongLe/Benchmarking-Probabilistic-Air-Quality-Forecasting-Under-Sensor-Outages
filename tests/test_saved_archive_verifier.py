"""Synthetic unit tests for the read-only verifier; no experiment data."""
import importlib.util
from pathlib import Path
import zipfile

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verify_saved_archive.py"
SPEC = importlib.util.spec_from_file_location("saved_archive_verifier", SCRIPT)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


@pytest.mark.parametrize("name", ["../escape", "/absolute", "C:/private", "x/../y", ""])
def test_reject_unsafe_names(name):
    with pytest.raises(ValueError):
        verifier.safe_name(name)


def test_windows_relative_path_is_normalized():
    assert verifier.safe_name("folder\\file.json") == "folder/file.json"


def test_reject_zip_traversal(tmp_path):
    path = tmp_path / "bad.zip"
    with zipfile.ZipFile(path, "w") as out:
        out.writestr("../escape", b"bad")
    with pytest.raises(ValueError):
        verifier.Archive(path)


def test_hash_tamper_detected(tmp_path):
    (tmp_path / "record.txt").write_text("actual")
    archive = verifier.Archive(tmp_path)
    with pytest.raises(ValueError, match="hash mismatch"):
        verifier.verify_mapping(archive, {"record.txt": "0" * 64}, prefix="")


def synthetic_metrics():
    runs, summary = [], []
    for model in ["persistence", "seasonal_naive_24h"] + [f"model_{n}" for n in range(10)]:
        seeds = [""] if model in {"persistence", "seasonal_naive_24h"} else [42, 123, 2026, 3407, 7777]
        for condition in range(8):
            for state in ["uncalibrated", "frozen_development_calibration"]:
                base = dict(model=model, condition=str(condition), calibration=state,
                            mase="1.0", observed_targets="10", valid_metric_cells="5")
                summary.append(base.copy())
                for seed in seeds:
                    runs.append(dict(base, seed=str(seed)))
    return runs, summary


def test_stored_mean_consistency():
    runs, summary = synthetic_metrics()
    assert verifier.verify_summary(runs, summary) == 192 * 3


def test_changed_summary_is_rejected():
    runs, summary = synthetic_metrics()
    summary[0]["mase"] = "2.0"
    with pytest.raises(ValueError, match="mean mismatch"):
        verifier.verify_summary(runs, summary)


def test_wrong_seeds_are_rejected():
    runs, summary = synthetic_metrics()
    next(row for row in runs if row["seed"] == "42")["seed"] = "99"
    with pytest.raises(ValueError, match="seeds"):
        verifier.verify_summary(runs, summary)
