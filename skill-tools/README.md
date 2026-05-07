# Skill Tools — Build & Upgrade Skills Safely

Create well-structured Claude Code skills and upgrade them with backup, audit, and rollback protection.

## Why

Skills are persistent rules that span sessions. A bad edit to a skill can silently corrupt behavior across all future sessions. Good skill hygiene means:

- **Structure**: every skill has the same essential sections so CC can reason about it reliably
- **Backup**: snapshot before any edit so you can always roll back
- **Audit**: mechanical checks catch accidental deletions and format breaks
- **Readers**: confirm all agents (CC, Codex) see the same version

## Tools

| Tool | What it does |
|------|-------------|
| `SKILL.md` | The meta-skill — CC loads this to guide skill creation and upgrade |
| `upgrade-guard.py` | Mechanical guard: preflight snapshot, audit, reader check, rollback |

## Install

```bash
# Symlink so CC can discover the skill
ln -s $(pwd)/skill-tools/SKILL.md ~/.claude/skills/skill-tools/SKILL.md
```

## Usage

### Create a new skill

Trigger: say "create skill <name>" and CC will follow the skill-tools protocol for structure, required sections, and quality standards.

### Upgrade an existing skill

```bash
# 1. Snapshot before editing
python3 upgrade-guard.py preflight my-skill --reason "fix broken trigger condition"

# 2. Edit the skill (manually or via CC)

# 3. Audit against the snapshot
python3 upgrade-guard.py audit my-skill

# 4. If you use Codex, sync and verify
# (use OpenClaude/skill-frontmatter/sync-skills.sh or your own rsync)
python3 upgrade-guard.py readers my-skill
```

### Rollback

```bash
# List available backups
python3 upgrade-guard.py list my-skill

# Restore latest
python3 upgrade-guard.py rollback my-skill
```

### Configuration

Defaults work for standard setups. Override via env vars:

| Variable | Default | Purpose |
|----------|---------|---------|
| `SKILLS_HOME` | `~/.claude/skills` | Canonical skills directory |
| `SKILLS_BACKUP` | `~/.claude/skill-backups` | Backup snapshots (outside skills dir) |
| `CODEX_SKILLS` | `~/.codex/skills` | Codex/OpenCode skills for reader check |

## Commands

```
upgrade-guard.py preflight <skill>        Create backup snapshot
upgrade-guard.py audit <skill>            Compare active vs snapshot
upgrade-guard.py readers <skill>          Check Codex copy matches
upgrade-guard.py rollback <skill>         Restore from backup
upgrade-guard.py list <skill>             List backups
```

## Requirements

- `python3` (stdlib only, no pip packages)
- `git` (optional — for recording git HEAD in manifest)
