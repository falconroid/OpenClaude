#!/bin/bash
# Sync skills from CC (or any source) to Codex (or any target).
# Codex doesn't follow symlinks (issue #8943), so we use rsync to copy real files.
# Run after skill updates.
#
# Usage:
#   ./sync-skills.sh                          # default paths
#   ./sync-skills.sh ~/mind/skills ~/.codex/skills
#   SOURCE=~/vault/mind/skills TARGET=~/.codex/skills ./sync-skills.sh
#
# Default paths can be set via env vars SOURCE and TARGET.
# Order: CLI args > env vars > defaults.

set -euo pipefail

SOURCE="${1:-${SOURCE:-$HOME/vault/mind/skills}}"
TARGET="${2:-${TARGET:-$HOME/.codex/skills}}"

if [ ! -d "$SOURCE" ]; then
    echo "ERROR: source not found: $SOURCE" >&2
    exit 1
fi

echo "→ Syncing skills from $SOURCE to $TARGET"

# --delete: remove skills in target that were deleted in source
# --exclude='.system': preserve Codex built-in system skills
# -L: dereference symlinks (Codex doesn't follow file symlinks, issue #8943)
#     Remove -L if your source has no symlinks (avoids self-reference loops)
rsync -avL --delete \
    --exclude='.system' \
    "$SOURCE/" "$TARGET/"

echo "→ Done. Skill count:"
find "$TARGET" -maxdepth 2 -name "SKILL.md" | wc -l

echo "→ Skills:"
find "$TARGET" -maxdepth 2 -name "SKILL.md" | sed "s|$TARGET/||" | sed 's|/SKILL.md||' | sort
