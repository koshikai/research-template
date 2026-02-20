# Daily Research Logs

This directory stores date-based experiment notes.

- File naming: `YYYY-MM-DD.md`
- One entry per experiment run
- Keep entries short and actionable (decision + next action)
- Use `uv run poe daily-report --request <path>` to write entries from report requests.

Recommended entry template:

```text
## YYYY-MM-DD HH:MM:SS - Experiment Name

- Summary: 1-2 line summary
- Decision: Pass/Fail/Continue
- Next Action: what to try next
- Thought Flow: hypothesis -> verification -> decision
- Notes: insights, hypotheses, key logs
- Output: outputs/<experiment>/<timestamp>/
- Report: outputs/<experiment>/<timestamp>/report.md
- Params: outputs/<experiment>/<timestamp>/params.json
- Metrics: key=value
```
