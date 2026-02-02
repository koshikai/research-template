import argparse
from pathlib import Path

from ai_research_template.core import LinearModel
from ai_research_template.data import generate_linear_data
from ai_research_template.metrics import compute_mse
from ai_research_template.utils import (
    current_timestamp,
    load_config,
    prepare_output_dir,
    save_params,
    save_results,
    setup_logger,
    update_experiment_summary,
    write_daily_report_request,
    write_report,
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
    output_dir_config = config.get("output_dir")
    if output_dir_config:
        base_dir = Path(output_dir_config)
        experiment_name = base_dir.name
        output_root = base_dir.parent
    else:
        experiment_name = config.get("experiment_name", "experiment")
        output_root = Path(config.get("output_root", "outputs"))

    timestamp = current_timestamp()
    output_dir = prepare_output_dir(
        experiment_name=experiment_name,
        output_root=output_root,
        timestamp=timestamp,
    )

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
    save_params(config, output_dir)
    update_experiment_summary(results, output_dir)
    write_report(
        [
            "# Experiment Report",
            "",
            f"- Timestamp: {timestamp}",
            f"- Experiment: {experiment_name}",
            f"- Output: {output_dir}",
            f"- MSE: {mse:.4f}",
        ],
        output_dir,
    )
    request_path = write_daily_report_request(
        output_dir=output_dir,
        experiment_name=experiment_name,
        timestamp=timestamp,
        config_path=args.config,
        metrics=results.get("metrics", {}),
    )

    logger.info(f"Experiment complete! Results saved to {output_dir}")
    logger.info(f"MSE: {mse:.4f}")
    logger.info(f"Estimated: y = {model.slope:.2f}x + {model.intercept:.2f}")
    logger.info("Daily report request written.")
    logger.info(f"Run: uv run poe daily-report --request {request_path}")


if __name__ == "__main__":
    main()
