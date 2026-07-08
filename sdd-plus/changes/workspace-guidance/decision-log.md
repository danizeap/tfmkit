# Decision Log

## Change

workspace-guidance

## Decisions

| Date | Decision | Reason | Alternatives Considered |
| --- | --- | --- | --- |
| 2026-07-08 | Files are the memory; every session re-orients from the workspace | Thesis spans ~10 days of sessions; context windows and app restarts make one-chat workflows fragile | Relying on a single long-lived session (loses detail on compaction; dies on restart) |
| 2026-07-08 | Template copied verbatim, not personalized by onboard | Keeps guidance deterministic and update-safe; personal data belongs in tfm.config.yaml | Generating a bespoke CLAUDE.md per project (drift, sanitization risk) |
