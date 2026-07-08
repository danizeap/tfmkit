---
name: ingest
description: Distill the student's curated source documents into traceable fact sheets with per-fact provenance. Use when the student adds materials to sources/, or before drafting any section that lacks a fact sheet.
---

# TFMkit Ingest — Sources → Fact Sheets

Fact sheets are the ONLY ground truth drafting is allowed to use. Your job here is
extraction, never creation.

## Procedure

1. Read each document in `sources/` the student points you to.
2. For each, produce/update a fact sheet in `facts/<topic-or-section>.md`:

```markdown
# Ficha de hechos — <topic>

Fuente(s): <filename(s)>

| ID | Hecho | Procedencia |
|----|-------|-------------|
| F1 | <one verifiable fact, in the author's terms, figures exact> | <file, section/page> |
| F2 | … | … |

## Huecos detectados
- [PENDIENTE: <what the sources do not say but the section will need>]

## Posible confidencialidad
- <term or figure that looks internal/NDA — flag for the student to decide>
```

3. Number facts sequentially and never renumber existing IDs — drafts reference them.
4. **Figures are sacred**: copy numbers, dates, and names exactly as the source states
   them. If two sources disagree, record both and mark `[VERIFICAR: fuentes discrepan]`.
5. Flag anything that smells confidential (internal names, non-public figures, third
   parties). Ask the student whether each flagged item goes into
   `confidentiality.banned_terms` in `tfm.config.yaml`.
6. Summarize to the student: how many facts, which gaps, which flags.

## Rules

- No fact without provenance. If you cannot say where it came from, it does not enter
  the sheet.
- Gaps are recorded as `[PENDIENTE: …]`, never filled by inference.
- Do not paraphrase figures or results into vaguer language; precision is the point.
