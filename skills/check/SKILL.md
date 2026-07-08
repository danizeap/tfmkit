---
name: check
description: Integrity and style check of a draft - AI-tell hunting with the metrics loop, external critic pass, safety gate on every edit round, lint and counters. Use after drafting a section or before publishing.
---

# TFMkit Check — Measure, Improve, Never Break Facts

Three passes: the **metrics loop** (style), the **critic** (substance), the **lint**
(remaining work). Deterministic scripts judge; you rewrite; the gate can veto you.

## 1. Metrics loop (bounded, default 2 rounds)

For the target file (e.g. `drafts/<section>.md`):

1. `python "${CLAUDE_PLUGIN_ROOT}/scripts/signals.py" <file> --config tfm.config.yaml`
   → scorecard + concrete offenders.
2. Rewrite the document attacking exactly those offenders, under these rails:
   - Do not change any figure, date, percentage, model name or proper noun.
   - Do not touch tables, code blocks, headings, or "Campo: valor" data lines.
   - Keep every `[PENDIENTE]` exactly; insert no editorial marks; add no em-dashes.
   - Keep scope/emphasis words (todos, cada, solo, únicamente…): they carry meaning.
   - Keep the academic register and the section's voice. Human ≠ sloppy.
   - Standard labels ("Fase 1:", "Indicador:") stay literal — they may be rubric items.
   - Craft: raise burstiness (short punchy sentences between long ones), vary sentence
     openings, break repeated n-grams EXCEPT mandatory technical terms, reduce abused
     connectors, choose the less predictable-but-precise word, break template phrasing.
     In first-person sections, add the author's voice and judgement — an aside, a real
     assessment — where the facts support it.
3. Write the candidate to a temp file and judge it:
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/gate.py" <before> <candidate> --config tfm.config.yaml`
   - Gate exits non-zero → **discard the round**, keep the previous version, tell the
     student in plain words which rail it broke (this is a feature, not a failure).
   - Gate passes → adopt the candidate, report the new scorecard, next round.
4. Stop when rounds are exhausted, the scorecard stops improving, or the gate rejects.

## 2. Critic pass (fresh eyes, marks only)

Invoke the `critic` subagent on the current version with the section's voice from
config. It returns the text with `[VERIFICAR]`/`[AÑADIR REFLEXIÓN]` marks — it never
rewrites. Walk the student through each mark; resolving them is the AUTHOR's work
(answers become new facts via `tfmkit:ingest`).

## 3. Lint and report

`python "${CLAUDE_PLUGIN_ROOT}/scripts/lint.py" <file> --config tfm.config.yaml`

When checking a single section draft, pass that section's word limits from
`tfm.config.yaml` (`sections[].limits`): `--min-words <n> --max-words <n>`. Violations
are blocking — the guidelines set them, not us.

Report to the student, in their language: unresolved markers, cliché hits, em-dashes,
flat-rhythm paragraphs, word counts vs limits, and any confidentiality hit (these are
blocking — the term must leave the text or the list, and that is the student's call
with their tutor, not yours).
