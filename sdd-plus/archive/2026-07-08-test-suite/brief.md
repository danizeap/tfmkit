# Brief

## Change

test-suite

## What this means for your product

After this change, any future edit that would weaken the integrity guardrails — the
gate, the lint, the signals, the typesetter — is caught by a 30-test suite before it
ever reaches a student.

## User Need

The deterministic scripts are the floor of the pyramid; regressions there are silent
integrity failures. Until now they were only proven by manual rehearsal runs.

## Problem

No automated tests existed. Every future change re-paid the manual verification cost.

## Scope

In scope: pytest suite (tests/) — 11 gate tests (every rail, rail-only rejection, soft
checks), 9 lint tests (markers, clichés, confidentiality, total and per-section limits,
blocking semantics), 5 signals tests (metrics, prose extraction, empty-doc, offenders),
6 publish tests (config-only cover, PENDIENTE placeholders, F-tag strip, heading styles,
PAGE field, TOC toggle). No product code changes.
Out of scope: CI pipeline (no hosted runner decision yet).

## Acceptance Criteria

- [x] `python -m pytest tests/ -q` → 30 passed.
- [x] Tests assert behavior (exit semantics, rail messages, docx content), not
      implementation details; fixtures are synthetic (no real personal/thesis data).
