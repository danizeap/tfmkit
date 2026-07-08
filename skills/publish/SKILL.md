---
name: publish
description: Assemble the final document and generate the .docx deliverable with config-driven cover and the AI-usage declaration. Use when the student wants the final document, or a preview of it.
---

# TFMkit Publish — Assemble and Typeset

## 1. Assemble

Concatenate the section drafts in the order defined by `sections[]` in
`tfm.config.yaml` into `final/tfm.md`. The abstract, if the guidelines require it, is
written LAST (it summarizes finished content) even though it is placed first.

## 2. Pre-flight (honesty gate)

Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/lint.py" final/tfm.md --config tfm.config.yaml`.

- Unresolved `[PENDIENTE]`/`[VERIFICAR]`/`[AÑADIR REFLEXIÓN]` markers or confidentiality
  hits are **blocking**: show each one to the student. Publishing with a known gap is
  the author's explicit decision, never a silent default.
- Check cover data in config (title, author, university, degree, year, tutors): any
  empty value will print as `[PENDIENTE: …]` on the cover — warn before generating.
- Confirm the AI-disclosure settings: `ai_disclosure.tool` should honestly name the
  tool used. If the student wants to omit the declaration, remind them once of their
  university's disclosure policy, then respect their decision (`include: false`).

## 3. Generate

`python "${CLAUDE_PLUGIN_ROOT}/scripts/publish.py" --in final/tfm.md --config tfm.config.yaml --out final/tfm.docx`

`[F#]` traceability tags are stripped automatically. Typography (font, size, spacing,
margins) comes from config — i.e. from the university's guidelines via `tfmkit:setup`.

## 4. Final review with the student

Open questions to walk through: does the section order match the guidelines' table of
contents? Are limits respected (lint reports counts)? Is the bibliography only verified
references (`references/bib.md`)? Then hand them the .docx and remind them: read it
whole — they sign it as the author.
