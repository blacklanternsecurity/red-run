#!/usr/bin/env bash
# Start shell-server as a persistent SSE service.
# Idempotent — exits silently if already running.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
PORT="${SHELL_SSE_PORT:-8022}"

# Skip if already listening
if ss -tln 2>/dev/null | grep -q ":${PORT} "; then
    exit 0
fi

exec uv run --directory "$REPO_DIR/tools/shell-server" python server.py
