#!/usr/bin/env bash
# Rebuild the local dev integration branch on top of main.
# Add feature branches to the array below as needed.
set -euo pipefail

BRANCHES=(
  docs/yolo-required
)

git checkout dev
git reset --hard main

if [ ${#BRANCHES[@]} -gt 0 ]; then
  git merge "${BRANCHES[@]}" --no-edit
fi

echo "dev rebuilt on main ($(git rev-parse --short HEAD))"
