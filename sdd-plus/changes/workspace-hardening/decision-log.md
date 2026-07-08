# Decision Log

## Change

workspace-hardening

## Decisions

| Date | Decision | Reason | Alternatives Considered |
| --- | --- | --- | --- |
| 2026-07-08 | Local git as the safety net, framed as "copias de seguridad automáticas" | Zero-cost history, no upload, invisible to the student | Timestamped copies only (kept as fallback); cloud backup (privacy + accounts) |
| 2026-07-08 | Snapshot rule lives in workspace CLAUDE.md, not in each skill | One rule loaded every session beats five duplicated instructions | Editing all five phase skills (drift risk) |
| 2026-07-08 | Section limits as lint flags, value passed by Claude from config | Drafts are one file per section; mapping headings to config keys inside lint is fuzzy | lint parsing sections[] and guessing which section the file is (fragile) |
