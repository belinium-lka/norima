#!/usr/bin/env bash
set -euo pipefail

# Simple installer: copies a shell script to ~/.local/bin/hello-sh
DEST_DIR="$HOME/.local/bin"
mkdir -p "$DEST_DIR"
SCRIPT_PATH="$DEST_DIR/hello-sh"

cat > "$SCRIPT_PATH" <<'SH'
#!/usr/bin/env bash
echo "Hello from hello-sh installed by noodle!"
SH

chmod +x "$SCRIPT_PATH"
echo "Installed hello-sh -> $SCRIPT_PATH"
