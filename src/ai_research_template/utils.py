"""Utility functions for experiment management.

This module provides helper functions for:
- Configuration loading (YAML files)
- Logging setup (file and console output)
- Result saving (JSON format)
- Experiment summary tracking (CSV format)
"""

import csv
import json
import logging
from pathlib import Path
from typing import Any

import yaml


def setup_logger(output_dir: Path, name: str = "experiment") -> logging.Logger:
    """Set up a logger that writes to both file and console.

    Creates a logger with two handlers:
    - File handler: writes detailed logs to {output_dir}/experiment.log
    - Console handler: writes simplified messages to stdout

    Args:
        output_dir: Directory where the log file will be created.
        name: Name of the logger (default: "experiment").

    Returns:
        Configured logger instance.

    Example:
        >>> logger = setup_logger(Path("outputs/exp1"))
        >>> logger.info("Starting experiment")
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers = []  # Clear existing handlers

    # File handler with detailed format
    fh = logging.FileHandler(output_dir / "experiment.log")
    fh.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(fh)

    # Console handler with simple format
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(ch)

    return logger


def update_experiment_summary(results: dict[str, Any], output_dir: Path) -> None:
    """Update the global experiment summary CSV file.

    Appends a new row to experiments.csv with flattened results.
    Keys are prefixed to indicate their source:
    - param_*: Configuration parameters
    - metric_*: Evaluation metrics
    - model_*: Model parameters

    Args:
        results: Dictionary containing 'config', 'metrics', and 'model_params' keys.
        output_dir: Directory of the current experiment (used to derive CSV path).

    Note:
        The CSV file is located at outputs/experiments.csv (parent of output_dir).
        If the CSV already exists with different columns, new columns will be
        added but existing rows may have empty values for new columns.
    """
    summary_path = output_dir.parent.parent / "experiments.csv"

    # Flatten the results for CSV
    flat_results: dict[str, Any] = {}

    # Add timestamp and path
    flat_results["timestamp"] = output_dir.name
    flat_results["path"] = str(output_dir)

    # Add config params (prefix with param_)
    for key, value in results.get("config", {}).items():
        if isinstance(value, (int, float, str, bool)):
            flat_results[f"param_{key}"] = value

    # Add metrics (prefix with metric_)
    for key, value in results.get("metrics", {}).items():
        if isinstance(value, (int, float, str, bool)):
            flat_results[f"metric_{key}"] = value

    # Add model params (prefix with model_)
    for key, value in results.get("model_params", {}).items():
        if isinstance(value, (int, float, str, bool)):
            flat_results[f"model_{key}"] = value

    # Read existing headers if file exists
    existing_headers: list[str] = []
    if summary_path.exists():
        with open(summary_path, newline="") as f:
            reader = csv.reader(f)
            existing_headers = next(reader, [])

    # Merge headers: existing + new columns
    all_keys = set(existing_headers) | set(flat_results.keys())
    fieldnames = sorted(all_keys)

    # If file exists, read all rows and rewrite with updated headers
    rows: list[dict[str, Any]] = []
    if summary_path.exists() and existing_headers:
        with open(summary_path, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    # Append new result
    rows.append(flat_results)

    # Write all rows with complete fieldnames
    with open(summary_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing the configuration parameters.

    Raises:
        FileNotFoundError: If the config file does not exist.
        yaml.YAMLError: If the file contains invalid YAML.

    Example:
        >>> config = load_config("configs/sample.yaml")
        >>> config["n_samples"]
        200
    """
    with open(config_path) as f:
        return yaml.safe_load(f)


def save_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save experiment results as a JSON file.

    Creates the output directory if it doesn't exist and saves
    the results to metrics.json with pretty formatting.

    Args:
        results: Dictionary containing experiment results.
        output_dir: Directory where metrics.json will be saved.

    Example:
        >>> results = {"metrics": {"mse": 0.05}, "config": {"lr": 0.01}}
        >>> save_results(results, Path("outputs/exp1"))
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "metrics.json", "w") as f:
        json.dump(results, f, indent=4)
