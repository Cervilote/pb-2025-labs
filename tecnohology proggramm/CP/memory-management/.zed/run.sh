#!/usr/bin/env bash
set -e

BINARY="$ZED_WORKTREE_ROOT/.zed/bin/$ZED_STEM"

if [[ ! -x "$BINARY" ]]; then
    echo "Binary not found: $BINARY"
    echo "Run Build first."
    exit 1
fi

echo "=== Running ==="
echo "$BINARY"
echo

"$BINARY"
