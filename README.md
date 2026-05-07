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

```bash
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

Then add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/home/YOUR_USER/.claude/statusline.sh",
    "refreshInterval": 10
  }
}
```

Replace `YOUR_USER` with your actual username.

## How It Works

Claude Code pipes a JSON object to the configured command on each refresh. The script reads `stdin`, extracts the relevant fields with `jq`, and prints a formatted single-line status.

The JSON includes model info, context window stats (`used_percentage`, `context_window_size`, `cache_read_input_tokens`), cost duration, effort level, thinking toggle, and session ID.

## Requirements

- `bash`
- `jq`
- Claude Code (obviously)
