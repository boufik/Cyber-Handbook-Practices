# 1. Directory structure

The Windows-equivalent folder of Linux's `~/.claude` is named `%USERPROFILE%\.claude`.

## 1a. Global structure: `C:\Users\username\.claude\`

```
.claude.json                    # App state, OAuth, UI toggles, personal MCP servers
.claude\
├── CLAUDE.md                   # Instructions for all projects
├── settings.json               # Permissions, hooks, env, model
├── keybindings.json
├── rules\                      # User-level topic rules
├── skills\                     # Personal skills (<name>\SKILL.md)
├── commands\                   # Personal /slash commands
├── agents\                     # Personal subagent definitions
├── workflows\                  # *.js orchestration scripts
├── output-styles\              # System-prompt variants
├── agent-memory\               # Subagent memory (memory: user)
├── themes\
├── plugins\                    # Installed plugins/marketplaces
├── history.jsonl               # Every prompt you've typed (up-arrow recall)
├── file-history\<session>\     # Pre-edit file snapshots for /rewind
├── plans\, debug\, tasks\, paste-cache\, image-cache\, uploads\,
│   session-env\, sessions\, shell-snapshots\, backups\, usage-data\
└── projects\
    └── C--Users-username-Documents-projectname\
        ├── <session-uuid>.jsonl          # <- the file you inspected
        ├── <session-uuid>\subagents\     # subagent transcripts
        ├── <session-uuid>\tool-results\  # large tool outputs spilled to disk
        └── memory\                       # <- the ACTUAL auto memory
            ├── MEMORY.md                 # index, loaded every session
            ├── user_role.md              # topic files, read on demand
            └── feedback_testing.md
```

The folder name is the working directory path with non-alphanumeric characters replaced by `-`.
Over 200 chars it gets truncated and a path hash appended.

## 2b. Project-specific structure: `<repo>\`

```
CLAUDE.md                       # or .claude\CLAUDE.md
CLAUDE.local.md                 # personal, gitignored
.mcp.json                       # team-shared MCP servers
.worktreeinclude
.claude\
├── settings.json               # committed
├── settings.local.json         # gitignored
├── rules\*.md                  # optional `paths:` frontmatter = conditional load
├── skills\<name>\SKILL.md
├── commands\*.md
├── agents\*.md
├── workflows\*.js
└── agent-memory\<agent>\MEMORY.md
```

# 2. The JSONL transcript

Under `.claude\projects\C--Users-username-Documents-projectname`, there are multiple JSONL files.
Inside these JSONL files, each JSON entry is a message, a tool call, a tool result, or metadata.
This is where user prompts are stored.
They turn up under `content` key.
Roughly:

```json
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"..."}]}}
{"type":"assistant","message":{"role":"assistant","content":[...],"usage":{...}}}
```

What it's for:

- `claude --continue` / `claude --resume` replays it back into the context window. That is the only time it acts like memory, only because you asked for it.
- `/rewind` checkpoints, `/export` command, token accounting and third-party viewers.

Caveats:

- The entry format is **internal and changes between releases**. Scripts that parse it directly will break. Use `/export`, `claude -p --output-format json`
  or the `transcript_path` field passed to hooks instead.
- **Plaintext, unencrypted.** Anything a tool read lands here, including `.env` contents and credentials printed by a command. OS file permissions are the
  only protection.
- Swept after `cleanupPeriodDays` (default 30). The `memory\` subfolder is excluded from that sweep.

# 3. Auto memory

Claude writes these itself when something looks worth keeping.
Four `type`s in the frontmatter: `user`, `feedback`, `project`, `reference`.
It deliberately skips anything derivable from the codebase or already stated in `CLAUDE.md`.

- Keyed by **git repository**, so all worktrees share one memory dir.
- `MEMORY.md` is an index. Detail lives in topic files read on demand.
- On by default. Toggle in `/memory` or `autoMemoryEnabled: false` in settings or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- Plain markdown: read, edit or delete it freely.

# 4. Precedence

`CLAUDE.md` files are **concatenated**, not overridden: managed policy → user → project → local, root of tree down to cwd.
`settings.json` is the opposite. It is merged key by key, the more specific wins.
`CLAUDE.md` is delivered as a user message after the system prompt.
It is context, not enforcement.
For guaranteed behavior use hooks or `permissions.deny`.

# 5. Useful commands

Read-only:

```
/memory      List and open memory files
/context     Show what actually loaded this session
/status      Health check
```

State-changing — these write or delete:

```
/init                                    Writes a CLAUDE.md
/compact                                 Replaces history with a summary
/clear                                   Ends the conversation (recoverable via /resume)
claude project purge <path>              DELETES transcripts + auto memory for a project
claude project purge <path> --dry-run    Preview only, deletes nothing
```

# 6. TL;DR

The `.jsonl` files are **transcripts (logs)**, NOT memory.
They are a record of what happened, written after the fact.
Claude does **not** read them at startup. ** The real cross-session memory is markdown, NOT JSON.**

| Layer | Who writes it | Loaded at session start? |
|---|---|---|
| `CLAUDE.md` | you | yes, every session |
| `.claude/rules/*.md` | you | yes (or on path match) |
| `memory/MEMORY.md` (auto memory) | Claude | yes, first 200 lines / 25 KB |
| `memory/*.md` topic files | Claude | no — read on demand |
| `<session-id>.jsonl` | Claude Code runtime | **no** — only on `--resume` |

Every session starts with a fresh context window. Anything that persists does so because a file is re-injected into that window at launch.
