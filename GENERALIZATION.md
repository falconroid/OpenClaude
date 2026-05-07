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

## Cross-Platform

All scripts must work on Windows, macOS, and Linux without extra toolchains.

### Python > bash

Bash scripts only run on Unix. Rewrite as Python (stdlib only, no pip deps) for cross-platform:

```bash
# Bad — Unix only
bash sync-skills.sh ~/.claude/skills ~/.codex/skills

# Good — all OS
python3 sync-skills.py ~/.claude/skills ~/.codex/skills
```

Exceptions: scripts invoked by CC itself (not the user's shell) don't need conversion — CC runs in Node.js on all platforms.

### Paths: Path.home() + env vars

Never hardcode Unix-style paths (`/home/`, `~/vault/`). Use:

```python
# Python
from pathlib import Path
home = Path.home()
claude_skills = Path(os.environ.get("SKILLS_HOME", home / ".claude" / "skills"))
```

`Path.home()` returns `C:\Users\name` on Windows, `/home/name` on Linux, `/Users/name` on macOS.

For SKILL.md instructions, use `~/.claude/skills/` — CC translates `~` to the correct path on each platform.

### Zero dependencies

Python stdlib only. No `pip install` required. Libraries to avoid:
- `requests` → `urllib`
- `rich`/`click`/`typer` → `argparse` + `print`
- `pyyaml` → manual frontmatter parsing

### Keep bash as fallback, mark as Unix-only

If a bash script already exists and works, keep it but:
- Name the Python version as the recommended path in docs
- Label bash version "Unix only"
