# Symbol Capture — CLAUDE.md Snippet

Copy the rules below into your `~/.claude/CLAUDE.md`. Customize the target paths to match your own knowledge system.

## Default Configuration

Uses `~/.claude/captures/` as the base directory. Creates it automatically on first use.

```markdown
## Symbol Capture

Messages starting with these single-character prefixes are routed before normal response:

- **! / !! / !!! — Stream capture**: Capture marked content to `~/.claude/captures/stream/YYYY-MM-DD.md`. 1-3 `!` = priority 1-3. Format: timestamp header + content.
- **& / && / &&& — Idea registration**: Register the idea to `~/.claude/captures/ideas/YYYY-MM-DD-short-topic.md`. 1-3 `&` = priority 1-3.
- **= / == / === — Trick registration**: Register the reusable technique to `~/.claude/captures/tricks/YYYY-MM-DD-short-topic.md`. 1-3 `=` = priority 1-3.
- *** / ** / *** — Moment highlight**: Append to `~/.claude/captures/moments.md` (summary + key quote) and create a full archive in `~/.claude/captures/stories/YYYY-MM-DD-topic.md`. 1-3 `*` = priority 1-3.
- **$ / $$ / $$$ — Publish candidate**: Create a pointer file in `~/.claude/captures/publish-candidates/` with source trace. 1-3 `$` = priority 1-3.
- **+ / ++ / +++ — Todo registration**: Register the TODO in your task system. 1-3 `+` = priority 1-3.
- **? / ?? / ??? — Vent / emotion**: Capture to `~/.claude/captures/stream/YYYY-MM-DD.md`, tagged `#vent`. Acknowledge the emotion first, then respond. 1-3 `?` = priority 1-3.

Symbols can combine: `*$` = highlight + publish candidate.

Capture-first rule: detect the symbol → route to the right file → then respond to the conversation. Never skip capture because "we'll do it later."
```

## Customizing

### Change base directory

Replace `~/.claude/captures/` with your own path:

```markdown
- `!` → `~/Obsidian/vault/stream/` 
- `&` → `~/Notes/ideas/`
- `*` → `~/Notes/moments.md`
```

### Add your own symbols

Follow the same pattern. Pick a character, define the routing, document it:

```markdown
- `@ / @@ / @@@` → mention log: append to `~/.claude/captures/mentions.md`
```

### Integrate with external tools

Any target that accepts file writes:

```markdown
- `&` → Notion database via API
- `+` → Linear/Todoist task creation
- `$` → Buffer/Typefully draft queue
```

## Starting Small

Don't deploy all 7 symbols at once. Start with 3 — the ones you feel the friction of NOT having:

1. `!` (stream) — "I wish I wrote that down"
2. `&` (idea) — "That's a good concept"
3. `+` (todo) — "I need to do something with this"

Add more as muscle memory forms.
