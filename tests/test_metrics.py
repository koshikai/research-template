"""Tests for metrics module."""

import numpy as np
import pytest

from ai_research_template.metrics import (
    compute_mae,
    compute_mse,
    compute_r2,
    compute_rmse,
)


class TestComputeMse:
    """Tests for compute_mse function."""

    def test_perfect_prediction(self):
        """MSE should be 0 for perfect predictions."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        assert compute_mse(y_true, y_pred) == 0.0

    def test_known_value(self):
        """Test MSE with known expected value."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 1.9, 3.2])
        # (0.1^2 + 0.1^2 + 0.2^2) / 3 = 0.06 / 3 = 0.02
        assert compute_mse(y_true, y_pred) == pytest.approx(0.02)

    def test_shape_mismatch(self):
        """MSE should raise error for mismatched shapes."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match="same shape"):
            compute_mse(y_true, y_pred)


class TestComputeRmse:
    """Tests for compute_rmse function."""

    def test_perfect_prediction(self):
        """RMSE should be 0 for perfect predictions."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        assert compute_rmse(y_true, y_pred) == 0.0

    def test_known_value(self):
        """Test RMSE with known expected value."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([2.0, 3.0, 4.0])
        # MSE = 1.0, RMSE = 1.0
        assert compute_rmse(y_true, y_pred) == pytest.approx(1.0)


class TestComputeMae:
    """Tests for compute_mae function."""

    def test_perfect_prediction(self):
        """MAE should be 0 for perfect predictions."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        assert compute_mae(y_true, y_pred) == 0.0

    def test_known_value(self):
        """Test MAE with known expected value."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([2.0, 3.0, 4.0])
        # |1| + |1| + |1| / 3 = 1.0
        assert compute_mae(y_true, y_pred) == pytest.approx(1.0)

    def test_mixed_errors(self):
        """Test MAE with mixed positive and negative errors."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([0.0, 3.0, 2.0])
        # |1| + |1| + |1| / 3 = 1.0
        assert compute_mae(y_true, y_pred) == pytest.approx(1.0)

    def test_shape_mismatch(self):
        """MAE should raise error for mismatched shapes."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match="same shape"):
            compute_mae(y_true, y_pred)


class TestComputeR2:
    """Tests for compute_r2 function."""

    def test_perfect_prediction(self):
        """R2 should be 1.0 for perfect predictions."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        assert compute_r2(y_true, y_pred) == pytest.approx(1.0)

    def test_mean_prediction(self):
        """R2 should be 0.0 when predicting the mean."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        mean_val = np.mean(y_true)
        y_pred = np.full_like(y_true, mean_val)
        assert compute_r2(y_true, y_pred) == pytest.approx(0.0)

    def test_worse_than_mean(self):
        """R2 should be negative for predictions worse than mean."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([10.0, 20.0, 30.0])  # Very bad predictions
        r2 = compute_r2(y_true, y_pred)
        assert r2 < 0

    def test_shape_mismatch(self):
        """R2 should raise error for mismatched shapes."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match="same shape"):
            compute_r2(y_true, y_pred)
