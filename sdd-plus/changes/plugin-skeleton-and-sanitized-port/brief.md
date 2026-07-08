# Brief

## Change

plugin-skeleton-and-sanitized-port

## What this means for your product

After this change, your friend can install TFMkit as a Claude Code plugin and run its
integrity guardrails on his real TFM today, and the repo can go public without leaking a
single SECPHO figure, UDIT detail, or personal name.

## User Need

The pilot (a non-technical student, ~10 days to submission, starting today) needs an
installable TFMkit plugin whose deterministic integrity floor — style signals, lint,
safety gate, docx typesetter — actually works. Daniel needs the port from his private
SECPHO agents to be provably sanitized so the repo can be MIT/public from the start.

## Problem

The proven pipeline lives in a private repo, hardcodes confidential SECPHO terms
(`BAD_TERMS`), personal author/tutor names, UDIT cover data, and calls the OpenAI API.
TFMkit has no code yet: no plugin manifest, no skills, no scripts, no config schema.

## Scope

In scope:

- Claude Code plugin skeleton: `.claude-plugin/plugin.json` manifest, `skills/` (the seven
  workflow skills), `agents/critic.md`, `scripts/`, `config/tfm.config.template.yaml`.
- Sanitized deterministic scripts (no LLM calls anywhere):
  - `signals.py` — burstiness/openers/n-grams/connectors analysis (ported nearly as-is).
  - `gate.py` — safety gate as a standalone before/after CLI; confidentiality list read
    from `tfm.config.yaml` (ships empty), figures/markers/em-dash rails.
  - `lint.py` — markers, AI clichés, flat-rhythm, counters against config limits.
  - `publish.py` — Markdown → docx, fully config-driven cover; generalized AI-disclosure
    template with no personal defaults.
- Skill bodies encoding the sanitized writer/editor/critic prompt rules and the workflow
  (interview-first drafting, [F#] traceability, [PENDIENTE] fail-closed, web-verified
  citations, gate-checked edit rounds).
- Section registry moved out of code into the config template (generic, no UDIT keys).

Out of scope:

- Figure engine, PDF typesetter, defense prep, multi-language (post-v0.1 per BRIEF).
- Marketplace packaging/distribution.
- Parsing any real university guidelines (that is the pilot's `setup` run, not this change).

## Acceptance Criteria

- [ ] `git grep` over the repo finds zero occurrences of any `BAD_TERMS` entry, the
      author/tutor names hardcoded in the original `publisher.py`, or SECPHO/UDIT-specific
      strings in product code (BRIEF/PROJECT_CONTEXT may name SECPHO/UDIT as history).
- [ ] No `openai`/`anthropic` import and no API-key reference anywhere in the product.
- [ ] `python scripts/signals.py <md>` prints a scorecard; `python scripts/gate.py
      <before> <after>` exits non-zero when a figure changes, a `[PENDIENTE]` vanishes,
      an em-dash is added, or a configured confidential term appears.
- [ ] `python scripts/lint.py <md>` reports markers/clichés/counters; `python
      scripts/publish.py` produces a .docx with cover data taken only from config.
- [ ] Plugin loads in Claude Code (valid manifest; skills and critic agent discovered).
- [ ] Original files under `secpho_intelligence_system/TFM/agents/` untouched.

## Impact Areas

- Backend: new deterministic Python scripts (stdlib + python-docx + PyYAML).
- Frontend: n/a.
- Data model: `tfm.config.template.yaml` schema (sections, limits, cover, confidentiality).
- API: n/a (no network calls in product).
- AI/model behavior: skills/agent govern Claude's drafting/critique behavior (fail-closed).
- Documentation: README already carries vision; skills self-document the workflow.
- Operations/security: sanitization is the security gate of this change; verifier must
  check it explicitly.

## Open Questions

- Exact `plugin.json` field set against the current Claude Code plugin spec (validated
  during implementation).
- Whether `setup` should support PDF guidelines directly in v0.1 or ask for text (pilot
  brings his guidelines today — decide with him).
