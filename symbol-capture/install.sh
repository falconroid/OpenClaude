#!/bin/bash
# Symbol Capture — one-command install + one-command activate
# curl -sSL https://raw.githubusercontent.com/falconroid/OpenClaude/main/symbol-capture/install.sh | bash

set -e

SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills/symbol-capture}"
BASE_URL="https://raw.githubusercontent.com/falconroid/OpenClaude/main/symbol-capture"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

echo "→ Installing symbol-capture to $SKILL_DIR"
echo ""

mkdir -p "$SKILL_DIR"

curl -sSL "$BASE_URL/SKILL.md" -o "$SKILL_DIR/SKILL.md"
echo "  ✓ SKILL.md"

mkdir -p "$SKILL_DIR/examples"
curl -sSL "$BASE_URL/examples/claude-md-snippet.md" -o "$SKILL_DIR/examples/claude-md-snippet.md"
echo "  ✓ examples/"

echo ""
echo "  Skill installed. One more step to activate:"
echo ""
echo "  ─────────────────────────────────────────"
echo ""
echo "    cat $SKILL_DIR/examples/claude-md-snippet.md >> ~/.claude/CLAUDE.md"
echo ""
echo "  ─────────────────────────────────────────"
echo ""
echo "  (This appends the symbol rules that make capture work.)"
echo "  (Customize the target paths in CLAUDE.md afterwards if you want.)"
