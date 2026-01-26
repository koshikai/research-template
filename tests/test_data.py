import numpy as np
from ai_research_template.data import generate_linear_data


def test_generate_linear_data_shape():
    n = 50
    x, y = generate_linear_data(n_samples=n)

    assert len(x) == n
    assert len(y) == n
    assert x.shape == (n,)
    assert y.shape == (n,)


def test_generate_linear_data_values():
    n = 1000
    slope = 3.0
    intercept = 5.0
    x, y = generate_linear_data(
        n_samples=n, slope=slope, intercept=intercept, noise_std=0.01
    )

    # 最小二乗法で簡易的に確認（ノイズが小さいのでほぼ一致するはず）
    est_slope = (y[-1] - y[0]) / (x[-1] - x[0])
    assert abs(est_slope - slope) < 0.1
