# Skill Frontmatter Fixer

Two tools for running Claude Code skills under Codex CLI.

## Problem

Codex has stricter YAML frontmatter validation than CC, and doesn't follow symlinks (issue [#8943](https://github.com/anthropics/codex/issues/8943)). If you share skills between CC and Codex, you'll hit:

- **"Skill not found"** — symlinked skills are invisible to Codex
- **"Invalid SKILL.md"** — unquoted colons, multi-line descriptions, double `---` blocks break Codex's YAML parser

## Tools

| Script | What it does |
|--------|-------------|
| `sync-skills.sh` | rsync skills from source to target (real files, not symlinks) |
| `fix-frontmatter.py` | Rewrite SKILL.md frontmatter to Codex-compatible YAML |

## Usage

### 1. Sync skills (replace symlinks with real files)

```bash
./sync-skills.sh ~/vault/mind/skills ~/.codex/skills
```

After this, run `fix-frontmatter.py` on the target.

### 2. Fix frontmatter

```bash
# Dry-run first
python fix-frontmatter.py ~/.codex/skills --check

# Apply fixes
python fix-frontmatter.py ~/.codex/skills
```

### Typical workflow

```bash
# After updating skills in source (CC):
./sync-skills.sh ~/vault/mind/skills ~/.codex/skills
python fix-frontmatter.py ~/.codex/skills
```

## What `fix-frontmatter.py` fixes

- **Unquoted special chars** in description (colons, `#`, `{}`, etc.) → wraps in quotes
- **Double `---` blocks** → collapses to single frontmatter block
- **Multi-line descriptions** (`|`, `>`, `"|"` block scalars) → single quoted line
- **Markdown-style frontmatter** (`## name: foo`) → proper YAML (`name: foo`)
- **Missing frontmatter entirely** → generates one from the first heading

## Requirements

- `bash`, `rsync`, `python3`
