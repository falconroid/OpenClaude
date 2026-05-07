---
name: skill-frontmatter
description: "Fix SKILL.md YAML frontmatter for Codex compatibility and sync skills from Claude Code to Codex"
version: 1.0.0
---

# Skill Frontmatter — Codex Compatibility

Fixes YAML frontmatter in SKILL.md files so they pass Codex's strict validation, and syncs skill directories (rsync real files since Codex doesn't follow symlinks).

## Trigger

"fix frontmatter" / "sync skills to codex" / "skill frontmatter" / "Codex skill sync"

## Workflow

### Step 1: Sync skills (rsync, dereference symlinks)

```bash
bash sync-skills.sh ~/vault/mind/skills ~/.codex/skills
```

### Step 2: Fix frontmatter

```bash
# Check first
python3 fix-frontmatter.py ~/.codex/skills --check

# Apply
python3 fix-frontmatter.py ~/.codex/skills
```

## Common Issues Fixed

| Issue | Example | Fix |
|-------|---------|-----|
| Special chars in description | `description: foo: bar` | `description: "foo: bar"` |
| Double --- blocks | `---\n---\nname:` | `---\nname:` |
| Multi-line desc | `description: \|\n  line1\n  line2` | `description: "line1 line2"` |
| Markdown-style fm | `## name: skillname` | `name: skillname` |
| Missing frontmatter | No `---` block at all | Generates from first heading |

## Why Codex needs this

- Codex YAML parser is stricter than CC's
- Codex [#8943](https://github.com/anthropics/codex/issues/8943): doesn't follow file symlinks
- Unquoted colons in YAML strings → parse failure → skill invisible
