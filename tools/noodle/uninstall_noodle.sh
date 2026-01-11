#!/usr/bin/env bash
set -euo pipefail

TARGET="$HOME/.local/bin/noodle"
if [ -L "$TARGET" ] || [ -e "$TARGET" ]; then
  rm -f "$TARGET"
  echo "Removed $TARGET"
else
  echo "$TARGET not found"
fi
