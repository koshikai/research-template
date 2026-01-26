import numpy as np
import pytest
from ai_research_template.core import LinearModel


def test_linear_model_fit():
    model = LinearModel()
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([1, 3, 5, 7, 9])  # y = 2x + 1

    model.fit(x, y)

    assert pytest.approx(model.slope) == 2.0
    assert pytest.approx(model.intercept) == 1.0


def test_linear_model_predict():
    model = LinearModel()
    model.slope = 2.0
    model.intercept = 1.0
    x = np.array([10, 20])

    y_pred = model.predict(x)

    expected = np.array([21.0, 41.0])
    np.testing.assert_allclose(y_pred, expected)
