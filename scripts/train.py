import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

from ai_research_template.core import ResearchModel


def main():
    parser = argparse.ArgumentParser(description="Simple training/experiment script.")
    parser.add_argument("--lr", type=float, default=0.01, help="Learning rate")
    args = parser.parse_args()

    # Setup paths
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = Path("outputs") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    # Update 'latest' symlink (linux)
    latest_link = Path("outputs/latest")
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    try:
        latest_link.symlink_to(
            output_dir.relative_to(latest_link.parent), target_is_directory=True
        )
    except Exception:
        # Fallback if symlink fails
        pass

    # Setup logging
    log_file = output_dir / "logs" / "experiment.log"
    log_file.parent.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)

    logger.info(f"Starting experiment with parameters: {args}")

    # Execution (Do)
    model = ResearchModel(learning_rate=args.lr)
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = model.run_computation(data)

    logger.info(f"Result computed: {result}")

    # Save artifacts (Checkpoint/Results)
    metrics = {"success": True, "final_value": result, "parameters": vars(args)}
    with open(output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # Automated check summary for the Agent
    with open(output_dir / "report.md", "w") as f:
        f.write("# Experiment Report\n\n")
        f.write(f"- Timestamp: {timestamp}\n")
        f.write("- Status: Success\n")
        f.write(f"- Result: {result}\n")

    logger.info(f"Experiment finished. Results saved to {output_dir}")


if __name__ == "__main__":
    main()
