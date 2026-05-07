---
name: statusline-setup
description: "Configure Claude Code statusline via settings.json. Cross-platform: Python (all OS) or bash (Unix). Trigger: set up statusline / install statusline / configure status bar."
version: 1.0.0
---

# Statusline Setup

Install a compact, real-time statusline for Claude Code that shows model, context usage, cache hits, session duration, effort level, and thinking status.

## What You Get

```
[deepseek-v4-pro] 45% 32k/180k/200k | 3m42s | 3T | cc-maintain | abc123...
```

Fields: `model` `ctx%` `cache_k/used_k/win_k` `duration` `effort` `T/t` `directory` `session_id`

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

### Unix only (bash + jq)

```bash
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

## How It Works

Claude Code passes a JSON object via stdin containing:
- `model.display_name` — current model name
- `context_window.used_percentage` — context usage 0-100
- `context_window.context_window_size` — total window tokens
- `context_window.current_usage.cache_read_input_tokens` — cache hit tokens
- `cost.total_duration_ms` — current turn duration in ms
- `effort.level` — effort setting (1-5)
- `thinking.enabled` — whether thinking mode is on
- `session_id` — current session ID

The script formats these into a single-line compact display. `T` = thinking on, `t` = thinking off.
