"""What the grader reads. Nothing else reaches it.

- the agent's scoring (/workdir/rescore/PSG-0417.csv, ~10 kB);
- the agent's note (/workdir/rescore/report.json);
- the workstation tool log, written only by the root-only tools
  (/usr/local/lib/psgsys/tool_log.json). The agent cannot read or edit it.
"""

SCORING_PATH = "/workdir/rescore/PSG-0417.csv"
REPORT_PATH = "/workdir/rescore/report.json"
LOG_PATH = "/usr/local/lib/psgsys/tool_log.json"

SUBMISSION_FILES: tuple[str, ...] = (SCORING_PATH, REPORT_PATH, LOG_PATH)

MAX_SUBMISSION_BYTES = 256 * 1024
