#!/usr/bin/env python3
"""Claude Code statusline — cross-platform (Python stdlib, replaces bash+jq).

Receives JSON via stdin from Claude Code, prints a formatted one-line status.
Usage: set statusLine.command to this script in ~/.claude/settings.json
"""
import json
import os
import sys
from pathlib import Path


def count_lines(path):
    try:
        with open(path, "rb") as f:
            return sum(chunk.count(b"\n") for chunk in iter(lambda: f.read(65536), b""))
    except OSError:
        return None


def fmt_size(n):
    if n >= 1048576:
        return f"{n / 1048576:.1f}M"
    if n >= 1024:
        return f"{round(n / 1024)}K"
    return f"{n}B"


def fmt_lines(n):
    if n >= 1000:
        return f"{n / 1000:.1f}kL"
    return f"{n}L"


def jsonl_info(session_id):
    cwd = os.getcwd().replace("\\", "-").replace("/", "-")
    path = Path.home() / ".claude" / "projects" / cwd / f"{session_id}.jsonl"
    try:
        stat = path.stat()
    except OSError:
        return ""
    lines = count_lines(str(path))
    if lines is None:
        return ""
    return f" | {fmt_lines(lines)} {fmt_size(stat.st_size)}"


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
    jsonl = jsonl_info(session) if session != "?" else ""

    print(
        f"[{model}] {used_pct}% {cache_k}k/{used_k}k/{win_k}k | "
        f"{dur_fmt} | {effort}{think_icon} | {dir_name} | {session}{jsonl}",
        flush=True,
    )


if __name__ == "__main__":
    main()
