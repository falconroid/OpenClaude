# Generalization Rules

How to take a skill from `~/vault/mind/skills/` and publish it here.

## Remove

| Category | Examples | Why |
|----------|---------|-----|
| Personal paths | `~/vault/mind/`, `/home/aegis/` | Not portable |
| Soul-vault protocol | stream capture, consolidation, episodes | Personal knowledge system |
| OpenClaw references | `~/.openclaw/`, `sync-soul-skills.sh` | Not a public tool |
| Feishu/Lark wiki | wiki sync, wiki lessons | Personal wiki |
| Project-specific scripts | `cc-maintain/scripts/` | Internal infrastructure |
| Hardcoded skill source | `~/vault/mind/skills/` | Replace with `SKILLS_HOME` env var |

## Keep

| Category | Why |
|----------|-----|
| Codex/OpenCode references | Public tool, many CC users also use Codex |
| Standard CC paths | `~/.claude/skills/`, `~/.claude/settings.json` |
| Upgrade guard mechanics | preflight/audit/readers/rollback are universally useful |
| Safety rules | Non-obvious operational knowledge |

## Patterns

### Env vars over hardcoded paths

```python
# Bad
SKILLS = Path.home() / "vault" / "mind" / "skills"

# Good
SKILLS = Path(os.environ.get("SKILLS_HOME", Path.home() / ".claude" / "skills"))
```

### Graceful degradation for optional readers

```python
# Bad
if not codex.exists():
    errors.append("Codex reader missing")

# Good
if not codex.exists():
    info.append("Codex: not present (ok if not using Codex)")
```

### SKILL.md references: external → optional

```markdown
# Bad (personal wiki as required reading)
Read `/home/aegis/vault/mind/wiki/lessons/skill-upgrade-discipline.md`

# Good (contextual note)
If you maintain a lessons log, review relevant past incidents before upgrading.
```
