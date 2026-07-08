---
name: cite
description: Build the state of the art and bibliography with every reference verified online before it is cited, in APA 7. Use when the student needs references, a literature review, or wants to add/check a citation.
---

# TFMkit Cite — Zero Unverified References

A fabricated citation ends an academic career. The rule is absolute: **no reference
enters the text or the bibliography until it has been verified on the web.**

## Verification protocol (per candidate reference)

1. WebSearch for the work. Confirm ALL of: authors (exact names), year, title, venue
   (journal/conference/publisher), and that the work actually exists and says what it
   will be cited for (check the abstract at minimum).
2. Prefer primary sources; capture the DOI or a stable URL.
3. Record verified references in `references/bib.md`:

```markdown
| Cita | Referencia APA 7 | Verificada | Fuente de verificación |
|------|------------------|-----------|------------------------|
| (Apellido, 2023) | Apellido, N. (2023). Título. *Venue*. https://doi.org/... | 2026-07-08 | <where you confirmed it> |
```

4. **Unverifiable → excluded.** Tell the student what could not be confirmed and why it
   was left out. Never soften this; suggest a verified alternative instead.
5. Never cite a source the student's text does not actually rely on (no ornament
   citations), and never cite what you have not checked *for this claim*.

## APA 7 form

- Parenthetical (Apellido, año, p. X) or narrative Apellido (año).
- Textual quote <40 words in quotation marks; ≥40 words as indented block, no marks.
- Paraphrase always carries author-year.
- Bibliography alphabetical, hanging indent, only works actually cited in the text.

## State of the art drafting

When drafting the literature review, follow `tfmkit:draft` rules (voice `impersonal`),
grounded in the verified table only. A claim about a paper you only saw in a search
snippet is a `[VERIFICAR]`, not a citation.
