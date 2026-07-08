# TFMkit — Product Brief (v0, exploration output)

> Captured 2026-07-06 after the exploration session. Status: decided, kickoff pending.
> Origin: Daniel's TFM writing agents (writer/editor/publisher) + the full workflow that produced
> a real, 51-page, verified, UDIT-guideline-compliant TFM.
> Working language: **English** for code, docs and process. The product's v0.1 target domain is
> **Spanish-language TFMs** (the pilot's thesis is Spanish; tells/lints are Spanish-calibrated).

## What it is

**TFMkit**: an open-source (MIT) Claude Code plugin that helps a student write their TFM (master's
thesis) with integrity — **the anti-ghostwriter**. It does not write the thesis for the student: it
interviews the author, distills THEIR materials into traceable fact sheets, drafts only from those
facts, verifies every citation on the web, hunts AI-text tells, checks THEIR university's guidelines,
and typesets the deliverable. The student remains the author.

## Decisions made

| Decision | Value | Why |
|---|---|---|
| License | **Open source, MIT** | "Siempre somos open source" (Daniel). Brand: governed AI engineering (sibling of Drydock). |
| Form | **Claude Code plugin** (skills + subagents + deterministic scripts + config) | Claude IS the writer/editor: zero API keys inside the product. |
| API keys | **None in the product** | Billing is the user's own config (subscription, or `ANTHROPIC_API_KEY` on CLI/IDE surfaces). |
| Target user | **Non-technical**, desktop app, regular subscription | The pilot doesn't know what a terminal is. Everything conversational; Python auto-provisioned by Claude. |
| Name | **TFMkit** | Chosen by Daniel 2026-07-06. |
| Pilot | Daniel's friend, with his real TFM | His university's guidelines = first real config. He is curating his source docs INTO PLAIN TEXT (Daniel's instruction). |

## Architecture (the Drydock pattern applied to thesis writing)

```
SKILLS (govern Claude — no LLM of their own)
  tfmkit:onboard    guided first run; asks university/guidelines/docs;
                    creates project structure; auto-provisions Python + deps
  tfmkit:setup      parses the university guidelines (PDF/text) -> tfm.config.yaml
  tfmkit:ingest     author's curated docs -> FACT SHEETS with per-fact provenance
                    + [PENDIENTE] gaps + confidentiality flags
  tfmkit:draft      interview -> per-section draft, ONLY from fact sheets/answers;
                    [F#] traceability; never invents
  tfmkit:cite       state of the art: every reference VERIFIED via WebSearch
                    (authors/year/venue) before it is cited; APA 7
  tfmkit:check      AI-tells lint (em-dashes, "no solo", connectors, clichés) +
                    counters (words/chars/abstract/bio) + confidentiality +
                    guideline compliance
  tfmkit:publish    docx/PDF per config (typography, margins, cover,
                    paginated TOC, page numbering from the Introduction)
SUBAGENTS
  critic            external critic in a fresh context: only MARKS, never rewrites
                    (the Drydock verifier equivalent)
DETERMINISTIC SCRIPTS (Python, no LLM — the floor of the pyramid)
  signals (burstiness/openers/n-grams/connectors), lint, counters,
  safety gate (did a figure change? did a [PENDIENTE] vanish? -> reject),
  docx/pdf typesetter, figure engine with overlap check (phase 2)
CONFIG
  tfm.config.yaml   university, section structure, limits (words/chars),
                    typography/margins, language, per-project CONFIDENTIALITY LIST
```

## Port map from the existing agents (SECPHO repo, `TFM/agents/` — gitignored)

| Source | Destination in TFMkit | ⚠️ Mandatory sanitization |
|---|---|---|
| `prompts/writer_system.md`, `editor_polish_system.md`, `editor_system.md` | Body of the draft/check/critic skills | Strip SECPHO / UDIT-memoria references |
| `signals.py` | Deterministic script as-is (Spanish-first; multi-language later) | — |
| `publisher.py` | Lint + docx generator | **Remove hardcoded author/tutors**; generalize the AI-disclosure template |
| `editor.py` | Deterministic gate (Claude runs the loop) | **DO NOT COPY `BAD_TERMS`: it contains confidential SECPHO names and figures.** Becomes a per-project list in config |
| `sections.py` | Section registry moved into `tfm.config.yaml` | Remove memoria.*/tfm.* specific keys |
| `md2pdf_rl.py` + `tfm_pdf_udit.py` (scratchpad) | Config-driven typesetter | Remove hardcoded UDIT cover/names |
| This session's workflow (fact sheets, adversarial verification, web citation verification, tells sweep, compliance counters) | Encoded INTO the skills | — |

## Non-negotiable principles (integrity IS the product)

1. Facts come from the author (curated docs + interview). A gap = `[PENDIENTE]`, never invention.
2. No reference goes in unverified online. Zero fabricated citations.
3. The critic marks; it never rewrites. The deterministic gate rejects rounds that alter figures/markers.
4. Confidentiality by design: per-project banned-terms list, enforced by the lint.
5. Honest disclosure: AI-usage declaration template available.
6. The student is the author. TFMkit is governed assistance, not a ghostwriter.

## v0.1 scope (for the pilot)

onboard → setup (the friend's guidelines) → ingest (his curated texts) → draft (chapter by chapter) →
cite → check → publish. Out of v0.1: figure engine, defense prep, multi-language, more university
templates.

## Pending / open

- Confirm the pilot's doc formats/volume/confidentiality (he is curating into plain text).
- Verify against current Claude Code docs: which surfaces accept API-key auth (for the README).
- Kickoff: `git init` + Drydock governance in THIS repo (third dogfooding) + first change
  (sanitized port + skills). Do NOT share the current scripts with anyone before sanitizing.
