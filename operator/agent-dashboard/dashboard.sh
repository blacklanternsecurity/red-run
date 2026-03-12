#!/usr/bin/env bash
# Multi-agent dashboard — auto-discovers Claude Code agent output files.
#
# Usage: bash operator/agent-dashboard/dashboard.sh
#        bash operator/agent-dashboard/dashboard.sh extra-label:/tmp/.../extra.output

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Derive tasks directory for agent browser
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENCODED="${PROJECT_DIR//\//-}"
TASKS_DIR="/tmp/claude-$(id -u)/${ENCODED}/tasks"

exec python3 "$SCRIPT_DIR/tail-agent.py" --dashboard --tasks-dir "$TASKS_DIR" "$@"
