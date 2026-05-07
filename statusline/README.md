# Claude Code Statusline

Compact, real-time statusline for Claude Code. Shows model, context usage, cache hits, session duration, effort level, and thinking status — all in one line.

```
[deepseek-v4-pro] 45% 32k/180k/200k | 3m42s | 3T | cc-maintain | abc123...
```

## Fields

| Segment | Meaning |
|---------|---------|
| `deepseek-v4-pro` | Current model display name |
| `45%` | Context window usage percent |
| `32k/180k/200k` | Cache read / Currently used / Window size (k tokens) |
| `3m42s` | Turn duration (formatted h/m/s) |
| `3` | Effort level (1-5) |
| `T` / `t` | Thinking enabled / disabled |
| `cc-maintain` | Current directory name |
| `abc123...` | Session ID (truncated) |

## Install

Pick your platform:

**Linux / macOS / WSL:**
```bash
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
# Use statusline.sh in settings.json command
```

**Windows (or cross-platform):**
```bash
cp statusline.py ~/.claude/statusline.py
# Use "python3 ~/.claude/statusline.py" in settings.json command
```

Then add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py",
    "refreshInterval": 10
  }
}
```

## Files

| File | Platform | Depends on |
|------|----------|------------|
| `statusline.py` | All (Win/Mac/Linux) | Python 3 (stdlib) |
| `statusline.sh` | Linux, macOS, WSL | bash + jq |

## Requirements

- `python3` (for cross-platform) OR `bash` + `jq` (Unix only)
- Claude Code
