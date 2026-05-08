# Symbol Capture

> Single-character prefixes that route thoughts to the right place — without leaving the conversation.

## Is this for you?

You have long, deep conversations with Claude Code. Insights surface mid-flow — a concept worth keeping, a todo that just emerged, a moment you want to remember. You tell yourself "I'll capture that later." Later comes, the heat is gone, the thought is fuzzy. You don't capture it.

If this never happens to you, skip this. This tool solves one specific problem: **the gap between having a thought and recording it**.

If you use Claude Code for quick tasks and close the session, you don't need this. If your sessions run for hours and you treat CC as a thinking partner, read on.

## What it looks like

Normal conversation vs. symbol capture:

```
User: I think the real issue with our architecture is that we
      conflate state and configuration too often.

# ↑ That insight is now gone unless you manually save it later.
```

```
User: ! I think the real issue with our architecture is that we
      conflate state and configuration too often.

# ↑ That insight was written to ~/.claude/captures/stream/2026-05-08.md
#   before the AI even responded.
```

One character. No slash-command. No leaving the flow. The AI detects the prefix, routes the content, then continues the conversation normally.

## How to use

Type a symbol at the start of a message. Repeat it for priority (`!!!` > `!!` > `!`). Combine symbols when something crosses categories (`*$` = highlight + publish candidate).

| Type | Symbol | Where it goes |
|------|--------|---------------|
| Insight / event | `!` | Stream journal (`YYYY-MM-DD.md`) |
| Idea / concept | `&` | Ideas folder |
| Trick / technique | `=` | Tricks folder |
| Moment / highlight | `*` | Moments file + full archive |
| Publish candidate | `$` | Publish candidates folder |
| Todo / action item | `+` | Your task system |
| Vent / emotion | `?` | Stream journal (tagged `#vent`) |

Real examples:

```
& 苏格拉底式追问在面试中 100% 稳定出现——这是认知内化的标志
```

```
* 川说"情绪是觉知的显影液"——这可能是整个 session 最重要的洞察
```

```
+ 把 symbol-capture 的 install.sh 补上
```

```
? 又被同一个模式困住了，这次甚至比上次更糟
```

## Install

```bash
curl -sSL https://raw.githubusercontent.com/falconroid/OpenClaude/main/symbol-capture/install.sh | bash
```

Then activate:

```bash
cat ~/.claude/skills/symbol-capture/examples/claude-md-snippet.md >> ~/.claude/CLAUDE.md
```

Restart Claude Code. Done.

**What just happened:** CC auto-discovers skills placed in `~/.claude/skills/`. The CLAUDE.md rules tell it to watch for symbol prefixes and route them.

## Customize

Edit the paths in your CLAUDE.md. Defaults write to `~/.claude/captures/`. Point them anywhere — Obsidian vault, Notion, a git repo.

## Start small

Don't deploy all 7 symbols. Start with the 3 you feel the friction of NOT having:

1. `!` — "I wish I had written that down"
2. `&` — "That concept is worth keeping"
3. `+` — "I need to do something with this"

Add more as muscle memory forms.

## Feedback

[Open an issue](https://github.com/falconroid/OpenClaude).
