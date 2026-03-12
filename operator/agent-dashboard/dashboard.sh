#!/usr/bin/env bash
# Multi-agent dashboard — auto-discovers Claude Code agent output files.
#
# Usage: bash dashboard.sh
#        bash dashboard.sh extra-label:/tmp/.../extra.output

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Derive tasks directory from cwd (matches Claude Code's convention)
ENCODED="${PWD//\//-}"
TASKS_DIR="/tmp/claude-$(id -u)/${ENCODED}/tasks"

exec python3 "$SCRIPT_DIR/tail-agent.py" --dashboard --tasks-dir "$TASKS_DIR" --project-dir "$PWD" "$@"
