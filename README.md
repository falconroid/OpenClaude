# OpenClaude

Self-contained packages for Claude Code. Each solves one specific problem that emerges when
you use CC as a thinking partner — not just a code generator.

## Is this for you?

**Yes** if you recognize any of these:

- Your CLAUDE.md has grown past 50 lines and you wonder if it's organized right
- You had an insight mid-conversation, didn't write it down, and lost it
- You upgraded a skill and accidentally deleted something important
- You use both Claude Code and Codex and your skills don't work in one of them
- You want to see context usage and model state at a glance without asking

**Probably not** if you use CC for quick one-shot tasks and close the session. These packages
solve problems that appear with depth and repetition.

## Packages

Pick the ones that match a problem you actually have.

| What you want | Package | Effort |
|--------------|---------|--------|
| See model, context, and cache in the status bar | [statusline](statusline/) | 5 min |
| Create skills with the right structure from the start | [skill-builder](skill-builder/) | read + apply |
| Safely upgrade skills — backup, audit, rollback | [skill-upgrade](skill-upgrade/) | read + script |
| Make your CC skills work in Codex | [skill-codexify](skill-codexify/) | 2 min |
| Capture insights mid-conversation with one character | [symbol-capture](symbol-capture/) | 1 min |

**skill-builder + skill-upgrade** are complementary: one teaches structure, one handles upgrades.
**symbol-capture** is standalone — install it and start using it immediately.

### [statusline](statusline/)

See what your agent is doing without asking. Shows model name, context usage, cache stats,
effort level, and thinking toggle — all in one compact terminal line. Three implementations:
Node.js (recommended), Python (all platforms), bash (Unix).

### [skill-builder](skill-builder/)

The structural standard for CC skills — 6 required sections, quality gates, frontmatter rules.
Use this before you write a skill. Also the design spec behind CC's `skill-creator`.

### [skill-upgrade](skill-upgrade/)

Upgrading a skill is a transaction, not an edit. Preflight snapshot → incremental change →
structure audit → changelog → reader sync → rollback. Built after 68% of a 590-line skill
was lost to "simplification."

### [skill-codexify](skill-codexify/)

Codex expects stricter YAML frontmatter and reads real files (not symlinks). This fixes
frontmatter format and rsyncs your CC skills to Codex. Python + bash scripts.

### [symbol-capture](symbol-capture/)

Single-character prefixes that route thoughts to files without leaving the conversation.
Type `!` before a line and it's captured to your journal before the AI responds. Seven
symbols (`!` `&` `*` `$` `+` `=` `?`) for insights, ideas, highlights, todos, and more.

```bash
curl -sSL https://raw.githubusercontent.com/falconroid/OpenClaude/main/symbol-capture/install.sh | bash
```

## How to use

1. **Identify** the problem you actually have. Not the one that sounds cool.
2. **Read** that package's README — each is self-contained with install steps.
3. **Install** — most are one or two commands. CC auto-discovers skills in `~/.claude/skills/`.
4. **Customize** paths and targets. Defaults work, but yours are better.

## Design principles

- **Self-contained.** No package depends on another. Each solves one problem.
- **File-first.** Everything persists to files. Restart your session — nothing's lost.
- **One-command install.** If getting started takes a README to explain the README, it's too complex.
- **CC-native.** Uses CC's built-in skill discovery. No plugin manager, no extra tooling.
- **Cross-platform.** Python for all platforms, bash for Unix, Node.js where it fits. Windows is tested.

## Feedback

[Open an issue](https://github.com/falconroid/OpenClaude/issues).

## License

MIT
