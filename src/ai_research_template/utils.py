"""Utility functions for experiment management.

This module provides helper functions for:
- Logging setup (file and console output)
- Result saving (JSON format)
"""

import json
import logging
import os
import platform
import subprocess
import sys
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from uuid import uuid4


def current_timestamp() -> str:
    """Return a filesystem-safe timestamp for experiment folders."""
    return datetime.now(UTC).strftime("%Y-%m-%d_%H%M%S")


def update_latest_symlink(latest_link: Path, target_dir: Path) -> None:
    """Update a symlink to point at the latest experiment output.

    Errors are ignored to keep the experiment flow robust on systems
    that don't support symlinks.
    """
    temporary_link = latest_link.with_name(f".latest-{uuid4().hex}")
    try:
        temporary_link.symlink_to(
            target_dir.relative_to(latest_link.parent), target_is_directory=True
        )
        temporary_link.replace(latest_link)
    except OSError:
        temporary_link.unlink(missing_ok=True)


def prepare_output_dir(
    experiment_name: str,
    output_root: Path | str = Path("outputs"),
    timestamp: str | None = None,
) -> Path:
    """Create a standardized output directory for an experiment.

    Layout:
      outputs/<experiment_name>/<run_id>/
        logs/
        artifacts/
        metrics.json
        params.json
        manifest.json
    """
    output_root_path = Path(output_root)
    exp_root = output_root_path / experiment_name
    ts = timestamp or current_timestamp()
    output_dir = exp_root / f"{ts}-{uuid4().hex}"
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "logs").mkdir(exist_ok=True)
    (output_dir / "artifacts").mkdir(exist_ok=True)

    return output_dir


def setup_logger(output_dir: Path, name: str = "experiment") -> logging.Logger:
    """Set up a logger that writes to both file and console.

    Creates a logger with two handlers:
    - File handler: writes detailed logs to {output_dir}/logs/experiment.log
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

    log_dir = output_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    # File handler with detailed format
    fh = logging.FileHandler(log_dir / "experiment.log")
    fh.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(fh)

    # Console handler with simple format
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(ch)

    return logger


def run_provenance(config_path: str | None = None) -> dict[str, Any]:
    """Capture the code and environment before running the computation."""
    repository = Path(__file__).resolve().parents[2]
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )
    lockfile = repository / "uv.lock"
    return {
        "schema_version": 1,
        "lock_sha256": sha256(lockfile.read_bytes()).hexdigest()
        if lockfile.is_file()
        else None,
        "started_utc": datetime.now(UTC).isoformat(),
        "git_commit": commit.stdout.strip() if commit.returncode == 0 else None,
        "git_dirty": bool(status.stdout) if status.returncode == 0 else None,
        "argv": sys.argv,
        "cwd": str(Path.cwd()),
        "config_path": config_path,
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


def complete_run(output_dir: Path, provenance: dict[str, Any]) -> None:
    """Publish a run once its parameter and metric files are readable."""
    for filename in ("params.json", "metrics.json"):
        path = output_dir / filename
        with path.open(encoding="utf-8") as file:
            if not isinstance(json.load(file), dict):
                raise ValueError(f"Expected a JSON object in {path}")
    manifest = {
        **provenance,
        "run_id": output_dir.name,
        "finished_utc": datetime.now(UTC).isoformat(),
        "params": "params.json",
        "metrics": "metrics.json",
    }
    pending = output_dir / f".manifest-{uuid4().hex}.tmp"
    try:
        pending.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        os.link(pending, output_dir / "manifest.json")
    finally:
        pending.unlink(missing_ok=True)
    update_latest_symlink(output_dir.parent / "latest", output_dir)
    update_latest_symlink(output_dir.parent.parent / "latest", output_dir)


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
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


def save_params(params: dict[str, Any], output_dir: Path) -> None:
    """Save experiment parameters as a JSON file."""
    with open(output_dir / "params.json", "w", encoding="utf-8") as f:
        json.dump(params, f, indent=4)
