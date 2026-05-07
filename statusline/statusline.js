#!/usr/bin/env node
// Claude Code statusline — Node.js (works wherever CC runs).
// CC pipes JSON to stdin, this prints a formatted one-line status.
"use strict";

const { homedir } = require("os");
const { statSync, openSync, readSync, closeSync } = require("fs");
const { join } = require("path");

function countLines(path) {
  let fd;
  try { fd = openSync(path, "r"); } catch { return null; }
  const buf = Buffer.alloc(65536);
  let lines = 0, bytesRead;
  while ((bytesRead = readSync(fd, buf, 0, buf.length, null)) > 0) {
    for (let i = 0; i < bytesRead; i++) {
      if (buf[i] === 10) lines++;
    }
  }
  closeSync(fd);
  return lines;
}

function fmtSize(bytes) {
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(1) + "M";
  if (bytes >= 1024) return Math.round(bytes / 1024) + "K";
  return bytes + "B";
}

function fmtLines(n) {
  if (n >= 1000) return (n / 1000).toFixed(1) + "kL";
  return n + "L";
}

function jsonlInfo(sessionId) {
  const cwd = process.cwd().replace(/[\/\\]/g, "-");
  const path = join(homedir(), ".claude", "projects", cwd, sessionId + ".jsonl");
  let stat;
  try { stat = statSync(path); } catch { return ""; }
  const lines = countLines(path);
  if (lines === null) return "";
  return ` | ${fmtLines(lines)} ${fmtSize(stat.size)}`;
}

let input = "";
process.stdin.setEncoding("utf-8");
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  let data;
  try {
    data = JSON.parse(input);
  } catch {
    process.stdout.write("[?]\n");
    return;
  }

  const model = data?.model?.display_name ?? "?";
  const usedPct = data?.context_window?.used_percentage ?? 0;
  const winSize = data?.context_window?.context_window_size ?? 0;
  const cacheRead = data?.context_window?.current_usage?.cache_read_input_tokens ?? 0;
  const durMs = data?.cost?.total_duration_ms ?? 0;
  const effort = data?.effort?.level ?? "?";
  const thinking = data?.thinking?.enabled ?? false;
  const session = data?.session_id ?? "?";

  const cacheK = Math.floor(cacheRead / 1000);
  const usedK = Math.floor((usedPct * winSize) / 100 / 1000);
  const winK = Math.floor(winSize / 1000);

  let durS = Math.floor(durMs / 1000);
  const durH = Math.floor(durS / 3600);
  durS %= 3600;
  const durM = Math.floor(durS / 60);
  durS %= 60;
  const durFmt = durH > 0 ? `${durH}h${durM}m` : durM > 0 ? `${durM}m${durS}s` : `${durS}s`;

  const thinkIcon = thinking ? "T" : "t";
  const dirName = process.cwd().split(/[\\/]/).pop();
  const jsonl = session !== "?" ? jsonlInfo(session) : "";
  const statusLine = `[${model}] ${usedPct}% ${cacheK}k/${usedK}k/${winK}k | ${durFmt} | ${effort}${thinkIcon} | ${dirName} | ${session}${jsonl}`;

  // On Windows with cmd/pwsh, stdout handles multibyte better with explicit newline
  process.stdout.write(statusLine + "\n");
});
