#!/bin/bash
# Claude Code statusLine
# Receives JSON via stdin from Claude Code

input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // "?"')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
win_size=$(echo "$input" | jq -r '.context_window.context_window_size // 0')
cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
dur_ms=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
effort=$(echo "$input" | jq -r '.effort.level // "?"')
thinking=$(echo "$input" | jq -r '.thinking.enabled // false')
session=$(echo "$input" | jq -r '.session_id // "?"')

cache_k=$((cache_read / 1000))
used_k=$(( (used_pct * win_size / 100) / 1000 ))
win_k=$((win_size / 1000))

dur_s=$((dur_ms / 1000))
dur_m=$((dur_s / 60))
dur_h=$((dur_m / 60))
if [ "$dur_h" -gt 0 ]; then
    dur_fmt="${dur_h}h$((dur_m % 60))m"
elif [ "$dur_m" -gt 0 ]; then
    dur_fmt="${dur_m}m$((dur_s % 60))s"
else
    dur_fmt="${dur_s}s"
fi

[ "$thinking" = "true" ] && think_icon="T" || think_icon="t"

dir_name=$(basename "$PWD")

# JSONL file info
jsonl=""
if [ "$session" != "?" ]; then
    proj_dir="${PWD//\//-}"
    jsonl_path="$HOME/.claude/projects/$proj_dir/${session}.jsonl"
    if [ -f "$jsonl_path" ]; then
        size=$(stat -c%s "$jsonl_path" 2>/dev/null || stat -f%z "$jsonl_path" 2>/dev/null || echo 0)
        lines=$(wc -l < "$jsonl_path" 2>/dev/null || echo 0)
        if [ "$size" -ge 1048576 ]; then
            size_fmt=$(awk "BEGIN {printf \"%.1fM\", $size/1048576}")
        elif [ "$size" -ge 1024 ]; then
            size_fmt="$(( (size + 512) / 1024 ))K"
        else
            size_fmt="${size}B"
        fi
        if [ "$lines" -ge 1000 ]; then
            lines_fmt=$(awk "BEGIN {printf \"%.1fkL\", $lines/1000}")
        else
            lines_fmt="${lines}L"
        fi
        jsonl=" | $lines_fmt $size_fmt"
    fi
fi

printf "[%s] %s%% %dk/%dk/%dk | %s | %s%s | %s | %s%s" \
    "$model" "$used_pct" "$cache_k" "$used_k" "$win_k" "$dur_fmt" "$effort" "$think_icon" "$dir_name" "$session" "$jsonl"
