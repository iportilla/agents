"""PreToolUse hook: block shell commands that could destroy lab data.

Claude Code runs this before every Bash tool call and passes the call as JSON
on stdin. Exit code 2 blocks the call, and what we print to stderr is shown to
Claude as the reason. Exit code 0 lets it through.

Unlike an instruction in CLAUDE.md, this runs every time: the model can't
argue with it or forget it.
"""

import json
import re
import sys

BLOCKED = [
    r"\brm\b",
    r"\bmv\b.*\.csv",
    r">\s*\S*\.csv",          # overwriting a CSV with a redirect
    r"\bgit\s+(push|reset\s+--hard|clean)\b",
]

call = json.load(sys.stdin)
command = call.get("tool_input", {}).get("command", "")

for pattern in BLOCKED:
    if re.search(pattern, command):
        print(
            f"Blocked by lab hook: '{command}' matches '{pattern}'. "
            "Lab data is read-only.",
            file=sys.stderr,
        )
        sys.exit(2)

sys.exit(0)
