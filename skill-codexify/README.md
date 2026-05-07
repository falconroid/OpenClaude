# Skill Codexify — Make CC Skills Work in Codex

Three tools for running Claude Code skills under Codex/OpenCode CLI.

## Problem

Codex has stricter YAML frontmatter validation than CC, and doesn't follow symlinks (issue [#8943](https://github.com/anthropics/codex/issues/8943)). If you share skills between CC and Codex, you'll hit:

- **"Skill not found"** — symlinked skills are invisible to Codex
- **"Invalid SKILL.md"** — unquoted colons, multi-line descriptions, double `---` blocks break Codex's YAML parser

## Tools

| Script | Platform | What it does |
|--------|----------|-------------|
| `sync-skills.py` | All (Python) | Copy skills as real files, resolving symlinks |
| `sync-skills.sh` | Unix | Same, via rsync |
| `fix-frontmatter.py` | All (Python) | Rewrite SKILL.md frontmatter to Codex-compatible YAML |

## Usage

### 1. Sync skills (cross-platform, recommended)

```bash
python3 sync-skills.py ~/.claude/skills ~/.codex/skills
# Or with env vars:
SOURCE=~/.claude/skills TARGET=~/.codex/skills python3 sync-skills.py
```

`--dry-run` to preview without changes.

### 2. Fix frontmatter

```bash
python3 fix-frontmatter.py ~/.codex/skills --check   # dry-run
python3 fix-frontmatter.py ~/.codex/skills            # apply
```

### Typical workflow

```bash
python3 sync-skills.py ~/.claude/skills ~/.codex/skills
python3 fix-frontmatter.py ~/.codex/skills
```

## What `fix-frontmatter.py` fixes

- **Unquoted special chars** in description (colons, `#`, `{}`, etc.) → wraps in quotes
- **Double `---` blocks** → collapses to single frontmatter block
- **Multi-line descriptions** (`|`, `>`, `"|"` block scalars) → single quoted line
- **Markdown-style frontmatter** (`## name: foo`) → proper YAML (`name: foo`)
- **Missing frontmatter entirely** → generates one from the first heading

## Requirements

| Script | Depends on | Notes |
|--------|-----------|-------|
| `sync-skills.py` | Python 3 (stdlib) | All OS, no pip |
| `sync-skills.sh` | bash + rsync | Unix only |
| `fix-frontmatter.py` | Python 3 (stdlib) | All OS, no pip |

## Related

- **[skill-builder](../skill-builder/)** — structure standards for creating new skills
- **[skill-upgrade](../skill-upgrade/)** — safe upgrade protocol. Step 6 (sync readers) uses this workflow
