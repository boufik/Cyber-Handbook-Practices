# Project rules for Claude Code

## 1. Git: The Absolute Boundary
* I must **manage `git` entirely on my own**. You must **NEVER** run `git add`, `git commit`, `git push`, `git pull`, `git checkout`, `git reset`, `git stash`, `git rebase`, `git merge`, `git branch`, `git switch`, or any other command that modifies repository state or working tree via git. So, no `git`-related commands for you.
* Read-only `git` inspection (`git status`, `git diff`, `git log`, `git show`) is allowed for you, mainly when needed for context.
* Do not suggest commit messages or PR descriptions unless I explicitly ask.
* *Summary*: I must retain **full control of `git`**, so you (the agent) must never run any `git` command that modifies the repository state.

---

## 2. Change workflow: Always Keep Me In The Loop
* Before writing or editing ANY file, **describe in plain text**:
   - Which files you intend to modify?
   - What the change does?
   - Why is the change needed?
   - Are there any side effects or files that might also need changes later?
* Wait for my explicit `"Go Ahead"` approval before making the edit.
* Make ONE logical change at a time. Do not batch unrelated edits.
* After each accepted edit, give me a **one-line summary of what changed**.
* Never run formatters, linters or test commands without asking me first.
* *Summary*: Before editing any file, you (the agent) must describe the planned change and wait for my explicit `"Go Ahead"` approval with one logical change at a time.

---

## 3. Scope Discipline
* Touch only files directly **related to the task** I described.
* If you think a change requires editing files outside the obvious scope, you must STOP and ASK me.
* Do not refactor "while you're in there." **Do not rename things I didn't ask to rename**.
* *Summary*: You must stay strictly within the scope of the requested task.

---

## 4. When Unsure
* Ask! Never guess! Never invent file paths, API names, or library functions!
* *Summary*: You must ask rather than guess when anything is unclear.

---

## 5. Sharding Large Outputs
The entire repository is pushed to GitHub. GitHub warns above 50 MB and **hard-rejects any file over 100 MB**.
Treat 50 MB as the hard ceiling for any generated output file.

### 5a. Rule
Any pipeline that writes an output file whose size scales with the input (records fetched, pages crawled, hosts scanned) MUST shard its output.
Do NOT wait to be asked! If a writer has no natural upper bound, build sharding into it from the start.

### 5b. Requirements
1. **Shard while writing, NOT after.** Track bytes written and roll over to the next shard when the next record would exceed the limit. Never materialise a 500 MB file and split it afterwards.
2. **Never split a record across shards.** Each shard must be independently parseable.
3. **Naming:** `<basename>_<NNN>.<ext>`, zero-padded from `001` (`findings_001.json` to `findings_014.json`). Zero-padding keeps lexicographic order equal to numeric order.
4. **Prefer line-delimited formats** (`.jsonl` / NDJSON) for append-heavy record streams. Rolling over is a clean file swap; with a top-level JSON array every shard needs its own `[` … `]` bookkeeping.
5. **Emit a manifest** (`findings_manifest.json`) listing shard filenames, record counts, byte sizes and the schema version. Consumers read the manifest, NOT a directory glob.
6. **Provide a reader helper** that reassembles shards transparently, so downstream code never hardcodes shard paths.
7. Make the shard size a **module-level constant** (`MAX_SHARD_BYTES`), NOT a magic number scattered through the writer.

### 5c. Cases where you should use sharding
- Bulk enrichment records ingested from an upstream advisory or feed, where a full sync produces hundreds of thousands of JSON document in one file.
- Scraped corpora, where each stored item carries high volume of information (e.g., full body text of a blog). A few thousand items is already well past the limit.
- Per-host scan results across a large address range, where output size is a function of the target list, NOT a constant.
- Any accumulating log or trace file written across repeated runs.
