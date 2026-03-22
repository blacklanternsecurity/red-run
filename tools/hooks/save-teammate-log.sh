#!/usr/bin/env bash
set -euo pipefail

# TeammateIdle hook — copies teammate JSONL transcripts to engagement evidence.
# Reads hook JSON from stdin. Exits silently if no engagement directory exists.
# Always exits 0 to never block the teammate.

INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

# No transcript path or file missing = nothing to copy
[[ -z "$TRANSCRIPT_PATH" ]] && exit 0
[[ ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# No engagement directory = no logging (graceful degradation)
LOG_DIR="engagement/evidence/logs"
[[ ! -d "$LOG_DIR" ]] && exit 0

TIMESTAMP=$(date -u '+%Y%m%dT%H%M%SZ')
SAFE_ID=$(echo "${SESSION_ID:-unknown}" | tr -cd 'a-zA-Z0-9-' | head -c 20)

# Copy transcript (teammate may continue, so this captures current state)
cp "$TRANSCRIPT_PATH" "${LOG_DIR}/${TIMESTAMP}-teammate-${SAFE_ID}.jsonl"
exit 0
