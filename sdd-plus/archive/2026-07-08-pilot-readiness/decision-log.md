# Decision Log

## Change

pilot-readiness

## Decisions

| Date | Decision | Reason | Alternatives Considered |
| --- | --- | --- | --- |
| 2026-07-08 | TOC/page numbers as Word field codes | Deterministic, no pagination engine needed; Word recomputes on F9/print | Computing pagination in Python (fragile, font-metric dependent) |
| 2026-07-08 | Numbering starts after cover, not at Introduction | Multi-section restart is fiddly in python-docx; acceptable for v0.1, revisit if the pilot's guidelines demand it | Full section-based numbering now (time cost before today's session) |
| 2026-07-08 | Quickstart in Spanish, in the repo root | The student is the reader; Daniel teaches from it today | English doc (wrong audience), wiki (invisible offline) |
