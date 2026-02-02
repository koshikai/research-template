"""Tests for utility functions."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from ai_research_template.utils import load_config, save_results, setup_logger


def test_load_config():
    """Test loading a YAML configuration file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config = {"n_samples": 100, "learning_rate": 0.01}
        yaml.dump(config, f)
        f.flush()

        loaded = load_config(f.name)

        assert loaded["n_samples"] == 100
        assert loaded["learning_rate"] == 0.01

    Path(f.name).unlink()


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
