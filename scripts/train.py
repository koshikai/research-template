import argparse

from ai_research_template.core import ResearchModel
from ai_research_template.utils import (
    current_timestamp,
    prepare_output_dir,
    save_params,
    save_results,
    setup_logger,
    write_daily_report_request,
    write_report,
)


def main():
    parser = argparse.ArgumentParser(description="Simple training/experiment script.")
    parser.add_argument("--lr", type=float, default=0.01, help="Learning rate")
    parser.add_argument(
        "--experiment-name", type=str, default="train", help="Experiment name"
    )
    parser.add_argument(
        "--output-root", type=str, default="outputs", help="Output root directory"
    )
    args = parser.parse_args()

    # Setup paths
    timestamp = current_timestamp()
    output_dir = prepare_output_dir(
        experiment_name=args.experiment_name,
        output_root=args.output_root,
        timestamp=timestamp,
    )

    # Setup logging
    logger = setup_logger(output_dir)

    logger.info(f"Starting experiment with parameters: {args}")

    # Execution (Do)
    model = ResearchModel(learning_rate=args.lr)
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = model.run_computation(data)

    logger.info(f"Result computed: {result}")

    # Save artifacts (Checkpoint/Results)
    metrics = {"success": True, "final_value": result}
    save_results(metrics, output_dir)
    save_params(vars(args), output_dir)
    write_report(
        [
            "# Experiment Report",
            "",
            f"- Timestamp: {timestamp}",
            f"- Experiment: {args.experiment_name}",
            "- Status: Success",
            f"- Result: {result}",
        ],
        output_dir,
    )
    request_path = write_daily_report_request(
        output_dir=output_dir,
        experiment_name=args.experiment_name,
        timestamp=timestamp,
        config_path=None,
        metrics=metrics,
    )

    logger.info(f"Experiment finished. Results saved to {output_dir}")
    logger.info("Daily report request written.")
    logger.info(f"Run: uv run poe daily-report --request {request_path}")


if __name__ == "__main__":
    main()
