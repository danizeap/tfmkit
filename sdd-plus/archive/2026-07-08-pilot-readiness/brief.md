# Brief

## Change

pilot-readiness

## What this means for your product

After this change, the .docx your friend submits has the cover, index, page numbers and
fonts his university expects, and he has a one-page Spanish guide to keep open while he
learns TFMkit today.

## User Need

Dress rehearsal (2026-07-08, full onboard→publish run with synthetic data) proved the
pipeline works but found the deliverable non-compliant: headings ignored the configured
font (Word theme default, colored), no page numbers, no table of contents — all three
promised in the founding brief. Separately, the non-technical pilot needs student-facing
Spanish documentation for today's first session.

## Problem

`publish.py` styled only the Normal style; heading styles, footer and TOC were absent.
No student-facing docs existed (README is for developers).

## Scope

In scope: heading styles from config (font, black, sized from base), PAGE field in the
footer (cover excluded via different-first-page), TOC field with "Índice" heading behind
`typography.include_toc` (default true), QUICKSTART.es.md, version 0.1.2.
Out of scope: page numbering restarting at the Introduction (v0.1 numbers all pages
after the cover; restart-at-section needs multi-section docx — post-pilot if guidelines
demand it).

## Acceptance Criteria

- [x] Generated docx: Heading 1-3 use the configured font, black, sized base+4/+2/+1.
- [x] Footer of every page except the cover carries a PAGE field.
- [x] TOC field present after the cover when include_toc (Word recomputes with F9).
- [x] QUICKSTART.es.md: Spanish, student-facing, no commands required, integrity framed
      as protection.
