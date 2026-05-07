---
name: statusline-setup
description: Configure Claude Code statusline via settings.json and statusline.sh
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

```bash
# 1. Copy the script
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh

# 2. Add to ~/.claude/settings.json
```

In `~/.claude/settings.json`, add:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/home/YOUR_USER/.claude/statusline.sh",
    "refreshInterval": 10
  }
}
```

Replace `YOUR_USER` with your actual username (or use `$HOME/.claude/statusline.sh` if Claude Code expands env vars).

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
