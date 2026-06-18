---
description: Build and maintain a repo-local Karpathy-style LLM wiki
---

Load the `llm-wiki` skill and execute that workflow now.

Use the current repo as the wiki workspace. Follow existing repo instructions first, including any existing `AGENTS.md`, `CLAUDE.md`, `.opencode/`, `raw/`, or `wiki/` conventions.

Additional request:

$ARGUMENTS

Interpret the first argument when present:

- `init`, `setup`, `bootstrap`: create or repair the wiki scaffold and repo schema.
- `ingest`, `add`, `import`, `source`: ingest files or URLs into `raw/sources/` and `wiki/`.
- `query`, `ask`, `answer`, or a natural-language question: answer from `wiki/index.md` first, then relevant wiki pages, then raw sources when needed.
- `lint`, `audit`, `health`, `check`: health-check the wiki and fix safe bookkeeping issues.

Core rules if the skill is not available in this session:

- Treat `raw/sources/` as immutable source truth and `wiki/` as LLM-maintained derived knowledge.
- Maintain `wiki/index.md` as the content index and `wiki/log.md` as the chronological log.
- Use Obsidian links like `[[page-name]]`, lowercase hyphenated filenames, and citations pointing back to raw files.
- When ingesting, update one page under `wiki/sources/` plus relevant pages under `wiki/concepts/`, `wiki/entities/`, `wiki/decisions/`, or `wiki/questions/`.
- When answering durable questions, prefer the wiki first and file reusable synthesis back into `wiki/` unless explicitly told not to write files.
- Do not ingest secrets, credentials, private keys, or sensitive personal data without asking first.

Return a compact summary of changed files, key takeaways, contradictions, open questions, and suggested next `/llm-wiki` command.
