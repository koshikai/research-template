"""Evaluation metrics for model assessment.

This module provides various metrics for evaluating model performance.
"""

import numpy as np


def compute_mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Mean Squared Error between true and predicted values.

    Args:
        y_true: Ground truth target values.
        y_pred: Predicted values from the model.

    Returns:
        The mean squared error as a float.

    Raises:
        ValueError: If y_true and y_pred have different shapes.

    Example:
        >>> y_true = np.array([1.0, 2.0, 3.0])
        >>> y_pred = np.array([1.0, 2.0, 3.0])
        >>> compute_mse(y_true, y_pred)
        0.0
    """
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"y_true and y_pred must have the same shape, "
            f"got {y_true.shape} and {y_pred.shape}."
        )
    return float(np.mean((y_true - y_pred) ** 2))


def compute_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Root Mean Squared Error between true and predicted values.

    Args:
        y_true: Ground truth target values.
        y_pred: Predicted values from the model.

    Returns:
        The root mean squared error as a float.

    Example:
        >>> y_true = np.array([1.0, 2.0, 3.0])
        >>> y_pred = np.array([2.0, 3.0, 4.0])
        >>> compute_rmse(y_true, y_pred)
        1.0
    """
    return float(np.sqrt(compute_mse(y_true, y_pred)))


def compute_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Mean Absolute Error between true and predicted values.

    Args:
        y_true: Ground truth target values.
        y_pred: Predicted values from the model.

    Returns:
        The mean absolute error as a float.

    Raises:
        ValueError: If y_true and y_pred have different shapes.

    Example:
        >>> y_true = np.array([1.0, 2.0, 3.0])
        >>> y_pred = np.array([2.0, 3.0, 4.0])
        >>> compute_mae(y_true, y_pred)
        1.0
    """
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"y_true and y_pred must have the same shape, "
            f"got {y_true.shape} and {y_pred.shape}."
        )
    return float(np.mean(np.abs(y_true - y_pred)))


def compute_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute R-squared (coefficient of determination) score.

    Args:
        y_true: Ground truth target values.
        y_pred: Predicted values from the model.

    Returns:
        The R-squared score as a float. Best possible score is 1.0.

    Raises:
        ValueError: If y_true and y_pred have different shapes.
    """
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"y_true and y_pred must have the same shape, "
            f"got {y_true.shape} and {y_pred.shape}."
        )
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return float(1 - (ss_res / ss_tot))
