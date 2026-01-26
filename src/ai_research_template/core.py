"""Core research logic implementation.

This module contains the main models and algorithms used in the research.
"""

import numpy as np


class LinearModel:
    """Simple linear regression model using ordinary least squares.

    Attributes:
        slope: The estimated slope of the linear model.
        intercept: The estimated intercept of the linear model.

    Example:
        >>> model = LinearModel()
        >>> x = np.array([1, 2, 3, 4, 5])
        >>> y = np.array([2, 4, 6, 8, 10])
        >>> model.fit(x, y)
        >>> model.predict(np.array([6]))
        array([12.])
    """

    def __init__(self) -> None:
        """Initialize the LinearModel with zero slope and intercept."""
        self.slope: float = 0.0
        self.intercept: float = 0.0

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Fit a linear model via analytic solution (ordinary least squares).

        Args:
            x: Input feature array of shape (n_samples,).
            y: Target value array of shape (n_samples,).

        Raises:
            ValueError: If x and y have different lengths or are empty.
        """
        if len(x) == 0 or len(y) == 0:
            raise ValueError("Input arrays must not be empty.")
        if len(x) != len(y):
            raise ValueError(
                f"x and y must have the same length, got {len(x)} and {len(y)}."
            )

        a = np.vstack([x, np.ones(len(x))]).T
        self.slope, self.intercept = np.linalg.lstsq(a, y, rcond=None)[0]

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict target values using the fitted linear model.

        Args:
            x: Input feature array of shape (n_samples,).

        Returns:
            Predicted values as an array of shape (n_samples,).
        """
        return self.slope * x + self.intercept


class ResearchModel:
    """A simple research model for experimental computations.

    This is a placeholder model that demonstrates the basic structure
    for research experiments.

    Attributes:
        learning_rate: The learning rate parameter for the model.
    """

    def __init__(self, learning_rate: float = 0.01) -> None:
        """Initialize the ResearchModel.

        Args:
            learning_rate: Learning rate for the model (default: 0.01).
        """
        self.learning_rate = learning_rate

    def run_computation(self, data: list[float]) -> float:
        """Run a simple computation on the input data.

        Args:
            data: A list of numerical values to process.

        Returns:
            The sum of data multiplied by the learning rate.
        """
        return sum(data) * self.learning_rate
