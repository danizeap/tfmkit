# Plan

## Change

pilot-readiness

## Approach

Extend build_docx: style Heading 1-3/Title from typography config; set
different_first_page and insert a PAGE field in the footer; insert a TOC field (+ Índice
heading) after the cover page break, gated by typography.include_toc. Add a shared
_field() helper for Word field codes. Add include_toc to the config template. Write
QUICKSTART.es.md. Bump 0.1.2.

## Files Expected To Change

scripts/publish.py · config/tfm.config.template.yaml · QUICKSTART.es.md (new) ·
.claude-plugin/plugin.json · .claude-plugin/marketplace.json

## Risks

TOC/PAGE are field codes: readers see them after Word updates fields (F9/print) — the
placeholder text explains this in Spanish. LibreOffice behavior may differ (untested).

## Rollback

Revert the commit; publish falls back to the 0.1.1 typesetter.
