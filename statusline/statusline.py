#!/usr/bin/env python3
"""Claude Code statusline — cross-platform (Python stdlib, replaces bash+jq).

Receives JSON via stdin from Claude Code, prints a formatted one-line status.
Usage: set statusLine.command to this script in ~/.claude/settings.json
"""
import json
import os
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        print("[?]", flush=True)
        return

    model = data.get("model", {}).get("display_name", "?")
    ctx = data.get("context_window", {})
    used_pct = ctx.get("used_percentage", 0)
    win_size = ctx.get("context_window_size", 0)
    cache_read = ctx.get("current_usage", {}).get("cache_read_input_tokens", 0)
    dur_ms = data.get("cost", {}).get("total_duration_ms", 0)
    effort = data.get("effort", {}).get("level", "?")
    thinking = data.get("thinking", {}).get("enabled", False)
    session = data.get("session_id", "?")

    cache_k = cache_read // 1000
    used_k = (used_pct * win_size // 100) // 1000
    win_k = win_size // 1000

    dur_s = dur_ms // 1000
    dur_m, dur_s = divmod(dur_s, 60)
    dur_h, dur_m = divmod(dur_m, 60)
    if dur_h > 0:
        dur_fmt = f"{dur_h}h{dur_m}m"
    elif dur_m > 0:
        dur_fmt = f"{dur_m}m{dur_s}s"
    else:
        dur_fmt = f"{dur_s}s"

    think_icon = "T" if thinking else "t"
    dir_name = os.path.basename(os.getcwd())

    print(
        f"[{model}] {used_pct}% {cache_k}k/{used_k}k/{win_k}k | "
        f"{dur_fmt} | {effort}{think_icon} | {dir_name} | {session}",
        flush=True,
    )


if __name__ == "__main__":
    main()
