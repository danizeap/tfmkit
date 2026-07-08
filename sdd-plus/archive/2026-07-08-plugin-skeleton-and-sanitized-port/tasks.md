# Tasks

## Change

plugin-skeleton-and-sanitized-port

## Implementation

- [x] Plugin manifest + marketplace file (mirroring Drydock's working shape).
- [x] `config/tfm.config.template.yaml` — full schema, empty confidentiality list.
- [x] Port `signals.py` (near as-is) with a CLI entry point.
- [x] Port `gate.py` — rails from `editor.py`, confidential terms from config only,
      LLM loop removed, exit code contract.
- [x] Port `lint.py` — markers/clichés/rhythm/counters from `publisher.py`.
- [x] Port `publish.py` — config-driven docx cover, generalized AI-disclosure template.
- [x] Seven skills + critic agent encoding the sanitized prompt rules and workflow.
- [x] Offline verification: fixtures prove signals/lint/gate/publish behavior incl.
      gate rejection paths.
- [x] Sanitization sweep: grep for every forbidden token (BAD_TERMS entries, personal
      names, tutor names, UDIT cover strings) over the whole repo → zero hits in product.
- [x] Verifier subagent review (FULL mode) — PASS WITH OPEN QUESTIONS, 2026-07-08.
- [x] Commit after verifier PASS.
