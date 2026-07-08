# Project Context

## Project Name

TFMkit

## Short Description

An open-source (MIT) Claude Code plugin that helps a student write their TFM (Spanish
master's thesis) with integrity — **the anti-ghostwriter**. It interviews the author,
distills THEIR materials into traceable fact sheets, drafts only from those facts, verifies
every citation on the web, hunts AI-text tells, checks the university's guidelines, and
typesets the deliverable. The student remains the author. Sibling of Drydock under the
"governed AI engineering" brand.

## Audience / Users

Non-technical students writing a TFM, using the Claude Code desktop app on a regular
subscription. The pilot user does not know what a terminal is: everything must be
conversational, with Python auto-provisioned by Claude during onboarding.

## Core Problem

Generative AI makes it trivial to produce a fake thesis and hard to produce an honest one.
Students need governed assistance: drafting grounded exclusively in their own facts,
verified citations, AI-tell removal, confidentiality enforcement, and guideline compliance —
without the tool becoming a ghostwriter.

## Desired Outcome

A student can go from curated source documents to a submitted, guideline-compliant,
integrity-verified TFM (docx/PDF) through the conversational workflow:
`onboard → setup → ingest → draft → cite → check → publish` — with zero API keys in the
product (Claude Code IS the model) and zero fabricated content.

## First Useful Version

v0.1 for the pilot: the full seven-skill workflow plus the critic subagent and the
deterministic script floor (signals, lint, counters, safety gate, docx typesetter),
config-driven via `tfm.config.yaml`. Out of v0.1: figure engine, defense prep,
multi-language, additional university templates.

## Stack And Tools

Preferred:

- Claude Code plugin structure: skills + subagents + deterministic Python scripts + config
- Python 3.11+ standard library where possible; `python-docx` for the typesetter
- YAML config (`tfm.config.yaml`) for everything university-/project-specific
- Drydock (SDD+) governance in this repo — third dogfooding project

Avoid:

- Any LLM API client inside the product (no API keys, no `openai`/`anthropic` packages)
- Hardcoding anything university-specific (UDIT), company-specific (SECPHO), or personal
- Heavy dependencies that complicate auto-provisioning on a non-technical user's machine

## Data And Integrations

- The author's curated source documents (plain text, per Daniel's instruction to the pilot)
- The university's TFM guidelines (PDF/text) — parsed into `tfm.config.yaml` by `setup`
- WebSearch (via Claude Code) for citation verification — every reference verified online
  (authors/year/venue) before it is cited; APA 7
- Reference-only source for the port: `secpho_intelligence_system/TFM/agents/` (NEVER
  modified, NEVER copied unsanitized, remains gitignored in its own repo)

## Constraints

- **Integrity IS the product** (non-negotiables): facts only from the author, `[PENDIENTE]`
  markers instead of invention; zero unverified citations; critic marks but never rewrites;
  deterministic gate rejects rounds that alter figures/markers; per-project confidentiality
  list enforced by lint; AI-usage disclosure template; the student is the author.
- **Sanitization (mandatory, from commit 1):** the original `BAD_TERMS` list is confidential
  (SECPHO names/figures) and must NEVER enter this repo — it becomes an empty per-project
  list in config. Hardcoded author/tutor names and UDIT cover data are stripped; the
  AI-disclosure template is generalized.
- **Zero API keys** in the product; billing is the user's own Claude subscription/config.
- **Timeline: HARD.** The pilot has ~10 days to submission (≈2026-07-18) and starts using
  TFMkit TODAY (2026-07-08). v0.1 must be minimally usable immediately; polish lands in
  daily increments while the pilot writes.
- v0.1 domain is Spanish-language TFMs (tells/lints Spanish-calibrated); code/docs in English.
- License MIT; repo public once sanitization is verified.

## Design / UX Preferences

Conversational, zero-terminal-knowledge assumed. The plugin explains what it is doing and
why at every step. Refusals (safety gate, missing facts) are explained in plain language as
integrity features, not errors. Spanish-facing output for the student; English internals.

## Definition Of Done

Kickoff phase: repo governed by Drydock; first change packet delivers the plugin skeleton
(manifest, skills/agents/scripts/config structure) and the sanitized deterministic scripts,
verified to contain zero SECPHO/UDIT/personal data. v0.1 phase: the pilot completes his real
TFM through the full workflow and submits it.

## Open Questions

- Pilot's doc formats/volume/confidentiality specifics (he is curating into plain text;
  confirm today when he arrives).
- Which Claude Code surfaces accept API-key auth (verify against current docs for the README).
- Marketplace/distribution path for the plugin after v0.1 (Drydock precedent).

## Durable Decisions

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-07-06 | License: open source, MIT | "Siempre somos open source"; governed-AI-engineering brand, sibling of Drydock |
| 2026-07-06 | Form: Claude Code plugin (skills + subagents + deterministic scripts + config) | Claude IS the writer/editor; zero API keys in the product |
| 2026-07-06 | Name: TFMkit | Chosen by Daniel |
| 2026-07-06 | Pilot: Daniel's friend with his real TFM | His university's guidelines become the first real config |
| 2026-07-06 | `BAD_TERMS` never enters this repo | Confidential SECPHO names/figures; becomes per-project config list |
| 2026-07-08 | Drydock governance from commit 1 (third dogfooding) | Practice what we ship; SDD+ gates guard the sanitization requirement |
| 2026-07-08 | v0.1 usable same-day; iterate daily during pilot | Pilot has ~10 days to submission and starts today |
