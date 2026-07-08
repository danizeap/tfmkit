# Decision Log

## Change

plugin-skeleton-and-sanitized-port

## Decisions

| Date | Decision | Reason | Alternatives Considered |
| --- | --- | --- | --- |
| 2026-07-08 | Repo root IS the plugin (manifest at root, governance alongside) | Matches Drydock 0.3.0's proven layout; single-repo install via marketplace `source: "./"` | Plugin in a `plugin/` subfolder (cleaner separation, but breaks the house convention and complicates install) |
| 2026-07-08 | Product scripts live in root `scripts/` next to governance `sdd.py` | Drydock precedent (its `scripts/` mixes plugin and release tooling); skills reference `${CLAUDE_PLUGIN_ROOT}/scripts/` | Separate `scripts/tfmkit/` namespace (adds a level for no user benefit) |
| 2026-07-08 | `common.py` not ported at all | It is the OpenAI API client; TFMkit has zero LLM calls — Claude Code is the model | Porting a stubbed version (dead code, invites key creep) |
| 2026-07-08 | Gate becomes a before/after CLI; Claude runs the edit loop | The original polish loop was LLM-in-Python; in the plugin the loop belongs to the `check` skill, the script only judges | Porting the loop with subprocess calls to Claude (violates zero-API-key architecture) |
| 2026-07-08 | Confidentiality list ships EMPTY in the config template | Original `BAD_TERMS` is SECPHO-confidential and must never enter this repo (BRIEF hard rule) | Shipping a redacted example list (still normalizes copying; zero value) |
| 2026-07-08 | Cliché/tells list IS ported | Generic Spanish/English AI-tells, no confidential content — it is the product's core lint | Config-only tells (loses the proven calibrated default) |
| 2026-07-08 | Script CLIs speak Spanish to the student, code/comments in English | v0.1 domain is Spanish TFMs; repo language is English (BRIEF) | All-English output (pilot is Spanish-speaking, non-technical) |
