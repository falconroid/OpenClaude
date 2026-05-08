# Claude Code Statusline

Compact, real-time statusline for Claude Code. Shows model, context usage, cache hits, session duration, effort level, and thinking status — all in one line.

```
[deepseek-v4-pro] 45% 32k/180k/200k | 3m42s | 3T | cc-maintain | abc123... | 4.1kL 6.5M
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
| `abc123...` | Session ID (full UUID) |
| `4.1kL 6.5M` | Session JSONL transcript: line count + file size (omitted if no transcript yet) |

## Install

### Recommended: Node.js (all platforms — CC already requires Node)

```bash
cp statusline.js ~/.claude/statusline.js
```

In `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/statusline.js",
    "refreshInterval": 10
  }
}
```

### Alternative: Python 3 (all platforms)

```bash
cp statusline.py ~/.claude/statusline.py
# Use: "python3 ~/.claude/statusline.py"
```

### Alternative: bash + jq (Unix only)

```bash
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
# Use: "~/.claude/statusline.sh"
```

## Files

| File | Platform | Depends on |
|------|----------|------------|
| `statusline.js` | All (Win/Mac/Linux) | Node.js (bundled with CC) |
| `statusline.py` | All (Win/Mac/Linux) | Python 3 (stdlib) |
| `statusline.sh` | Linux, macOS, WSL | bash + jq |

## Requirements

| Version | Depends on | Notes |
|---------|-----------|-------|
| `statusline.js` | Node.js (stdlib) | Guaranteed if CC is installed |
| `statusline.py` | Python 3 (stdlib) | No pip packages |
| `statusline.sh` | bash + jq | Unix only |

## Feedback

Found a bug or have a feature request? [Open an issue](https://github.com/falconroid/OpenClaude).
