#!/usr/bin/env bash
# Launch red-run: starts shell-server, then Claude Code.
set -euo pipefail
cd "$(dirname "$0")"
bash tools/shell-server/start.sh

# Parse run.sh-specific flags, pass the rest to claude
lead="ctf"
claude_args=()
for arg in "$@"; do
    case "$arg" in
        --yolo)       claude_args+=("--dangerously-skip-permissions") ;;
        --lead=*)     lead="${arg#--lead=}" ;;
        *)            claude_args+=("$arg") ;;
    esac
done

# Map lead to slash command, inject as initial prompt via system prompt
case "$lead" in
    ctf)    skill="/red-run-ctf" ;;
    legacy) skill="/red-run-legacy" ;;
    *)      echo "Unknown lead: $lead (options: ctf, legacy)" >&2; exit 1 ;;
esac

exec claude "${claude_args[@]}" \
    --append-system-prompt "On activation, immediately invoke the skill: ${skill}"
