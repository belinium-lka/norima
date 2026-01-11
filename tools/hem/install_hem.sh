#!/usr/bin/env bash
set -euo pipefail

# Install a small wrapper `hem` in ~/.local/bin which sets PYTHONPATH
# so the repository's `tools` package is importable without pip-install.
DEST_DIR="$HOME/.local/bin"
mkdir -p "$DEST_DIR"
REPO_ROOT="$(realpath "$(dirname "$0")/../..")"
TARGET="$DEST_DIR/hem"

if [ -L "$TARGET" ] || [ -e "$TARGET" ]; then
  echo "Removing existing $TARGET"
  rm -f "$TARGET"
fi

cat > "$TARGET" <<'SH'
#!/usr/bin/env bash
# wrapper to ensure repo root is on PYTHONPATH then exec hem
REPO_ROOT="__REPO_ROOT__"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "$REPO_ROOT/tools/hem/hem" "$@"
SH

sed -i "s|__REPO_ROOT__|$REPO_ROOT|g" "$TARGET"
chmod +x "$TARGET"
echo "Installed hem wrapper -> $TARGET (PYTHONPATH set to $REPO_ROOT)"
