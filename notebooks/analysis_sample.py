import marimo

__generated_with = "0.19.6"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from ai_research_template.data import generate_linear_data
    from ai_research_template.core import LinearModel
    from ai_research_template.metrics import compute_mse

    return LinearModel, compute_mse, generate_linear_data, mo, np, plt


@app.cell
def __(mo):
    mo.md("# Linear Regression Sample Analysis")
    return


@app.cell
def __(mo):
    s_n_samples = mo.ui.slider(10, 500, value=200, label="Number of samples")
    s_noise = mo.ui.slider(0.1, 2.0, step=0.1, value=0.8, label="Noise Std Dev")
    mo.hstack([s_n_samples, s_noise])
    return s_n_samples, s_noise


@app.cell
def __(generate_linear_data, s_n_samples, s_noise):
    x, y = generate_linear_data(
        n_samples=s_n_samples.value, slope=2.5, intercept=-1.0, noise_std=s_noise.value
    )
    return x, y


@app.cell
def __(LinearModel, x, y):
    model = LinearModel()
    model.fit(x, y)
    y_pred = model.predict(x)
    return model, y_pred


@app.cell
def __(compute_mse, mo, model, y, y_pred):
    mse = compute_mse(y, y_pred)
    mo.md(
        f"""
        ### Results
        - **MSE**: {mse:.4f}
        - **Estimated Slope**: {model.slope:.4f} (True: 2.5)
        - **Estimated Intercept**: {model.intercept:.4f} (True: -1.0)
        """
    )
    return (mse,)


@app.cell
def __(plt, x, y, y_pred):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, alpha=0.5, label="Data")
    ax.plot(x, y_pred, color="red", linewidth=2, label="Prediction")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.set_title("Linear Regression Fit")
    ax
    return ax, fig


if __name__ == "__main__":
    app.run()
