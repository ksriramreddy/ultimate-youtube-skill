#!/usr/bin/env bash
# Install the Ultimate YouTube skill for Claude Code (macOS / Linux).
#   ./install.sh            -> ~/.claude/skills/ultimate-youtube (all projects)
#   ./install.sh --project  -> ./.claude/skills/ultimate-youtube (current project only)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/skills/ultimate-youtube"
if [[ "${1:-}" == "--project" ]]; then
  DEST="$(pwd)/.claude/skills/ultimate-youtube"
else
  DEST="${HOME}/.claude/skills/ultimate-youtube"
fi

if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "error: run this from the repository root (SKILL.md not found at $SRC)" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
if [[ -d "$DEST" ]]; then
  echo "Updating existing install at $DEST"
  rm -rf "$DEST"
fi
cp -R "$SRC" "$DEST"
find "$DEST" -name "__pycache__" -type d -prune -exec rm -rf {} +
echo "Installed skill to $DEST"

if command -v uv >/dev/null 2>&1; then
  echo "uv found: scripts can run with 'uv run' and need no pip install."
else
  PY="$(command -v python3 || command -v python || true)"
  if [[ -z "$PY" ]]; then
    echo "warning: Python 3.10+ not found. Install Python, then: pip install -r $DEST/requirements.txt"
  else
    echo "Installing Python dependencies with $PY ..."
    "$PY" -m pip install --user -r "$DEST/requirements.txt" || \
      echo "warning: pip install failed. Try a virtualenv, or install uv (https://docs.astral.sh/uv/)."
  fi
fi

echo
echo "Next: open Claude Code and say \"set up the YouTube skill\"."
