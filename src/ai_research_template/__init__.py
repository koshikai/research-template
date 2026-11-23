"""AI Research Template - A template for AI-driven research projects.

This package provides core functionality for conducting reproducible
research experiments with AI agent collaboration.

Main modules:
    - core: Core models and algorithms (LinearModel)
    - data: Data generation and loading utilities
    - metrics: Evaluation metrics (MSE, RMSE, MAE, R2)
    - utils: Configuration, logging, and result management
"""

from ai_research_template.core import LinearModel
from ai_research_template.data import generate_linear_data
from ai_research_template.metrics import (
    compute_mae,
    compute_mse,
    compute_r2,
    compute_rmse,
)

__all__ = [
    "LinearModel",
    "compute_mae",
    "compute_mse",
    "compute_r2",
    "compute_rmse",
    "generate_linear_data",
]

__version__ = "0.1.0"
