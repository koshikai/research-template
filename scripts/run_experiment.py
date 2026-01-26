import argparse
from datetime import datetime
from pathlib import Path

from ai_research_template.core import LinearModel
from ai_research_template.data import generate_linear_data
from ai_research_template.metrics import compute_mse
from ai_research_template.utils import (
    load_config,
    save_results,
    setup_logger,
    update_experiment_summary,
)


def main():
    parser = argparse.ArgumentParser(
        description="Run a sample linear regression experiment."
    )
    parser.add_argument(
        "--config", type=str, default="configs/sample.yaml", help="Path to config file"
    )
    args = parser.parse_args()

    # 1. Load config
    config = load_config(args.config)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = Path(config["output_dir"]) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup logger
    logger = setup_logger(output_dir)
    logger.info(f"Starting experiment: {timestamp}")
    logger.info(f"Config: {config}")

    # 2. Generate data
    x, y = generate_linear_data(
        n_samples=config["n_samples"],
        slope=config["slope"],
        intercept=config["intercept"],
        noise_std=config["noise_std"],
    )

    # 3. Fit model
    model = LinearModel()
    model.fit(x, y)

    # 4. Evaluate
    y_pred = model.predict(x)
    mse = compute_mse(y, y_pred)

    # 5. Save results
    results = {
        "config": config,
        "metrics": {"mse": mse},
        "model_params": {
            "estimated_slope": float(model.slope),
            "estimated_intercept": float(model.intercept),
        },
    }
    save_results(results, output_dir)
    update_experiment_summary(results, output_dir)

    logger.info(f"Experiment complete! Results saved to {output_dir}")
    logger.info(f"MSE: {mse:.4f}")
    logger.info(f"Estimated: y = {model.slope:.2f}x + {model.intercept:.2f}")


if __name__ == "__main__":
    main()
