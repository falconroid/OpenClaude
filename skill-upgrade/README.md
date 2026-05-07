# Skill Upgrade

Safely upgrade existing Claude Code skills with backup, audit, reader sync, and rollback.

## Why

Skills are persistent rules. A bad edit silently corrupts behavior across all future sessions. Git gives you repo-level history, but doesn't prevent accidents at edit time — it won't stop you from deleting a critical section, won't check if all readers (CC, Codex) are consistent, and won't create an operation-level snapshot with a manifest.

This tool gives you those guardrails.

## vs. Official skill-creator

The official `skill-creator` plugin handles creation and iteration. It does NOT address the operational problem of **changing a skill that's already live**:

| Scenario | Official skill-creator | Skill Upgrade (this) |
|----------|----------------------|---------------------|
| Edit a live skill safely | Not covered | Preflight snapshot + incremental edit + audit |
| Prevent accidental section deletion | Not covered | `audit` blocks >20% line loss + missing headings |
| Confirm all readers in sync | Not covered | `readers` checks CC/Codex hash match |
| Rollback a bad edit | No mechanism | `rollback` with pre-rollback safety snapshot |
| Know what changed and why | Not covered | Mandatory CHANGELOG with driver/changes/verified |

This is the operational layer that sits below skill-creator's design layer.

## Usage

```bash
# 1. Snapshot before editing
python3 upgrade-guard.py preflight my-skill --reason "fix broken trigger"

# 2. Edit the skill

# 3. Audit against the snapshot
python3 upgrade-guard.py audit my-skill

# 4. Sync readers (if using Codex)
python3 upgrade-guard.py readers my-skill

# Rollback if needed
python3 upgrade-guard.py rollback my-skill
```

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `SKILLS_HOME` | `~/.claude/skills` | Canonical skills directory |
| `SKILLS_BACKUP` | `~/.claude/skill-backups` | Backup snapshots (outside skills dir) |
| `CODEX_SKILLS` | `~/.codex/skills` | Codex/OpenCode skills for reader check |

## Commands

```
upgrade-guard.py preflight <skill> [--reason "..."]    Create backup snapshot
upgrade-guard.py audit <skill> [--allow-rewrite]        Compare active vs snapshot
upgrade-guard.py readers <skill>                        Check Codex copy matches
upgrade-guard.py rollback <skill> [--backup <id>]       Restore from backup
upgrade-guard.py list <skill>                           List backups
```

## Requirements

- `python3` (stdlib only, no pip packages)
- Optional: `git` (for recording git HEAD in manifest)
