# Symbol Capture — Zero-Friction Idea Capture in Conversation

Tag thoughts, ideas, moments, and todos mid-conversation with single-character prefixes. Your AI routes them to the right place automatically.

```
!  insight that should live somewhere
&  idea / lightbulb moment
*  moment worth remembering
+  something to do later
```

Like keyboard shortcuts for your thinking stream.

## Why

The half-life of a good thought in conversation is seconds. By the time you finish talking and go back to capture it, the heat is gone. Symbols let you capture in the same instant you think.

## How It Works

You type a symbol prefix. Your AI (Claude Code, Codex, etc.) detects it and routes the content to the right file — stream journal, ideas folder, task system — before continuing the conversation.

**Capture first, respond second.**

## Install

```bash
curl -sSL https://raw.githubusercontent.com/falconroid/OpenClaude/main/symbol-capture/install.sh | bash
```

That downloads the skill into `~/.claude/skills/symbol-capture/`. One more command to activate:

```bash
cat ~/.claude/skills/symbol-capture/examples/claude-md-snippet.md >> ~/.claude/CLAUDE.md
```

Customize the target paths in CLAUDE.md afterwards. Restart Claude Code — done.

**What just happened:** CC auto-discovers skills in `~/.claude/skills/`. The CLAUDE.md rules tell it to watch for symbol prefixes and route them automatically.

## Default Symbols

| Symbol | Channel | Default Target |
|--------|---------|---------------|
| `!` / `!!` / `!!!` | Stream capture | `~/.claude/captures/stream/YYYY-MM-DD.md` |
| `&` / `&&` / `&&&` | Idea / lightbulb | `~/.claude/captures/ideas/YYYY-MM-DD-topic.md` |
| `=` / `==` / `===` | Trick / technique | `~/.claude/captures/tricks/YYYY-MM-DD-topic.md` |
| `*` / `**` / `***` | Moment / highlight | `~/.claude/captures/moments.md` |
| `$` / `$$` / `$$$` | Publish candidate | `~/.claude/captures/publish-candidates/` |
| `+` / `++` / `+++` | Todo | Your task system |
| `?` / `??` / `???` | Vent / emotion | `~/.claude/captures/stream/YYYY-MM-DD.md` (#vent) |

Repeat count = priority (`!!!` > `!!` > `!`). Symbols combine (`*$` = highlight + publish candidate).

## Configuration

All paths are yours to define. Edit the rules in your CLAUDE.md to point at your own knowledge system — local files, Obsidian, Notion, anything.

## Design Principles

- **Capture-first**: detect and route before responding
- **Zero friction**: one character, no slash-command, no leaving the flow
- **Err on capture**: false positive (over-capture) costs less than false negative (missed insight)
- **Heat half-life**: if you don't capture it now, the feeling is gone
- **Write side + read side = system**: every symbol defines who writes, who reads, and the trigger

## Requirements

- Claude Code (or any AI agent that follows CLAUDE.md rules)

## Feedback

Found a bug or have a feature request? [Open an issue](https://github.com/falconroid/OpenClaude).
