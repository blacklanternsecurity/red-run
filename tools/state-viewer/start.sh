#!/usr/bin/env bash
# Start the state-viewer web dashboard with default settings.
#
# Usage:
#   bash tools/state-viewer/start.sh
#
# For custom options, run the server directly:
#   python3 tools/state-viewer/server.py --port 9000 --db /path/to/state.db

exec python3 "$(dirname "$0")/server.py" "$@"
