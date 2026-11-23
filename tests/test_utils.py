"""Tests for utility functions."""

import json
import tempfile
from pathlib import Path

import pytest

from ai_research_template.utils import (
    complete_run,
    prepare_output_dir,
    save_params,
    save_results,
    setup_logger,
)


def test_save_results():
    """Test saving results to JSON file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        results = {"metrics": {"mse": 0.05}, "config": {"lr": 0.01}}

        save_results(results, output_dir)

        metrics_path = output_dir / "metrics.json"
        assert metrics_path.exists()

        with open(metrics_path) as f:
            loaded = json.load(f)

        assert loaded["metrics"]["mse"] == 0.05


def test_setup_logger():
    """Test logger setup creates log file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        logger = setup_logger(output_dir)

        assert logger is not None
        assert (output_dir / "logs" / "experiment.log").exists()

        logger.info("Test message")


def test_run_completion_keeps_incomplete_runs_out_of_latest(tmp_path: Path) -> None:
    timestamp = "2026-01-01_000000"
    completed = prepare_output_dir("sample", tmp_path, timestamp)
    incomplete = prepare_output_dir("sample", tmp_path, timestamp)

    assert incomplete != completed
    assert not (tmp_path / "latest").exists()

    save_params({}, completed)
    save_results({}, completed)
    complete_run(completed, {"git_commit": "example"})
    manifest = json.loads((completed / "manifest.json").read_text())
    assert manifest["run_id"] == completed.name
    assert manifest["git_commit"] == "example"
    assert (tmp_path / "latest").resolve() == completed
    assert (tmp_path / "sample/latest").resolve() == completed
    assert not (incomplete / "manifest.json").exists()

    save_params({}, incomplete)
    with pytest.raises(FileNotFoundError):
        complete_run(incomplete, {"git_commit": "example"})
    assert (tmp_path / "latest").resolve() == completed
    assert not (incomplete / "manifest.json").exists()

    save_results({}, incomplete)
    complete_run(incomplete, {"git_commit": "example"})
    with pytest.raises(FileExistsError):
        complete_run(completed, {"git_commit": "changed"})
    assert json.loads((completed / "manifest.json").read_text()) == manifest
    assert (tmp_path / "latest").resolve() == incomplete
    assert (completed / "manifest.json").exists()
