---
name: setup
description: Parse the student's university TFM guidelines (PDF or text) into tfm.config.yaml. Use when the student provides their guidelines, wants to configure sections/limits/typography, or needs to update the project configuration.
---

# TFMkit Setup — Guidelines → Config

Turn the university's OWN guidelines into `tfm.config.yaml`. Nothing is assumed: every
value comes from the guidelines document or from the student. TFMkit ships no university.

## Procedure

1. Read the guidelines document the student provided (in `sources/`). If it is a PDF,
   read it directly; if unreadable, ask the student to paste the relevant pages.
2. Extract, citing where in the guidelines each item comes from:
   - **Section structure**: every required section, in order, with its official
     requirements *in the guidelines' own words* → `sections[]` (key, title,
     requirements, limits). Assign `voice` per section: `primera` for personal
     experience/reflection sections, `impersonal` for theory/method/results,
     `mixta` where both apply.
   - **Limits**: word/page/abstract limits → `limits` and per-section `limits`.
   - **Typography**: font, size, spacing, margins → `typography`.
   - **Cover data requirements**: what the cover must show.
3. Interview the student for what guidelines cannot know (one question at a time):
   title (may stay empty), author name, degree, academic year, tutors, and the
   **confidentiality list** — explain it: terms that must never appear in the published
   text (employer internals, partner names, non-public figures). Empty is a valid answer.
4. Write `tfm.config.yaml`. Show the student a plain-language summary of what was
   configured and ask them to confirm the section list matches their guidelines.

## Rules

- Never invent a requirement. If the guidelines are silent on something (e.g. margins),
  leave the template default and tell the student it is a neutral default, not their
  university's rule.
- If guidelines conflict with the template defaults, guidelines win.
- Do not proceed to drafting until the student confirms the section list.
