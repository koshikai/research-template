"""Data generation and loading utilities.

This module provides functions for generating synthetic data
and loading real datasets for research experiments.
"""

import numpy as np


def generate_linear_data(
    n_samples: int = 100,
    slope: float = 2.0,
    intercept: float = 1.0,
    noise_std: float = 0.5,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate sample linear data with Gaussian noise.

    Creates synthetic data following the equation: y = slope * x + intercept + noise

    Args:
        n_samples: Number of data points to generate.
        slope: True slope of the linear relationship.
        intercept: True intercept of the linear relationship.
        noise_std: Standard deviation of the Gaussian noise.
        seed: Random seed for reproducibility. If None, results are not reproducible.

    Returns:
        A tuple of (x, y) where:
            - x: Input features as a 1D numpy array of shape (n_samples,).
            - y: Target values as a 1D numpy array of shape (n_samples,).

    Raises:
        ValueError: If n_samples is less than 1.

    Example:
        >>> x, y = generate_linear_data(n_samples=100, slope=2.0, intercept=1.0)
        >>> len(x), len(y)
        (100, 100)
    """
    if n_samples < 1:
        raise ValueError(f"n_samples must be at least 1, got {n_samples}.")

    if seed is not None:
        np.random.seed(seed)

    x = np.linspace(0, 10, n_samples)
    noise = np.random.normal(0, noise_std, n_samples)
    y = slope * x + intercept + noise
    return x, y
