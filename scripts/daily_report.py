import argparse
import json
import sys
from pathlib import Path
from typing import Any

from ai_research_template.utils import append_daily_log


def load_request(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def summarize_metrics(metrics: dict[str, Any]) -> str:
    metrics_source = metrics
    if isinstance(metrics.get("metrics"), dict):
        metrics_source = metrics["metrics"]

    items: list[str] = []
    for key, value in metrics_source.items():
        if isinstance(value, (int, float, str, bool)):
            items.append(f"{key}={value}")
    return ", ".join(items) if items else "n/a"


def get_value(value: str | None, prompt: str) -> str:
    if value is not None:
        return value
    if not sys.stdin.isatty():
        return "TBD"
    try:
        entered = input(f"{prompt}: ").strip()
    except EOFError:
        return "TBD"
    return entered or "TBD"


def resolve_request_path(args: argparse.Namespace) -> Path:
    if args.request:
        return Path(args.request)
    if args.output_dir:
        return Path(args.output_dir) / "report_request.json"
    return Path("outputs/latest/report_request.json")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write an AI-authored daily report entry."
    )
    parser.add_argument(
        "--request",
        type=str,
        default=None,
        help="Path to report_request.json (default: outputs/latest).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output dir containing report_request.json.",
    )
    parser.add_argument("--summary", type=str, default=None, help="One-line summary.")
    parser.add_argument(
        "--decision",
        type=str,
        default=None,
        help="Pass/Fail/Continue.",
    )
    parser.add_argument(
        "--next-action",
        type=str,
        default=None,
        help="Next action to take.",
    )
    parser.add_argument("--notes", type=str, default=None, help="Extra notes.")
    args = parser.parse_args()

    request_path = resolve_request_path(args)
    if not request_path.exists():
        raise SystemExit(f"Request file not found: {request_path}")

    request = load_request(request_path)
    timestamp = request.get("timestamp")
    if not isinstance(timestamp, str) or "_" not in timestamp:
        raise SystemExit("Invalid or missing timestamp in request file.")

    date_str, time_str = timestamp.split("_", maxsplit=1)
    time_fmt = f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"

    experiment_name = request.get("experiment_name", "experiment")
    output_dir = request.get("output_dir", "")
    report_path = request.get("report_path", "")
    params_path = request.get("params_path", "")
    config_path = request.get("config_path")
    metrics_summary = summarize_metrics(request.get("metrics", {}))

    summary = get_value(args.summary, "Summary")
    decision = get_value(args.decision, "Decision (Pass/Fail/Continue)")
    next_action = get_value(args.next_action, "Next action")
    notes = get_value(args.notes, "Notes")

    entry_lines = [
        f"## {date_str} {time_fmt} - {experiment_name}",
        "",
        f"- Summary: {summary}",
        f"- Decision: {decision}",
        f"- Next Action: {next_action}",
        f"- Notes: {notes}",
        f"- Output: {output_dir}",
        f"- Report: {report_path}",
        f"- Params: {params_path}",
        f"- Metrics: {metrics_summary}",
    ]
    if config_path:
        entry_lines.append(f"- Config: {config_path}")

    log_path = append_daily_log(entry_lines, log_date=date_str)
    print(f"Wrote daily report entry to {log_path}")


if __name__ == "__main__":
    main()
