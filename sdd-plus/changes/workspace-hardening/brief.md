# Brief

## Change

workspace-hardening

## What this means for your product

After this change, your friend can never lose a version of his thesis (every change is
snapshotted locally), his section word limits are enforced by the machine instead of by
eye, and the roughest install moment on a fresh Windows laptop is handled for him.

## User Need

Pilot starts today on an unknown Windows laptop, works ~10 days, and cannot be expected
to protect his own files or count words against his university's per-section limits.

## Problem

(1) The workspace had no version history: one bad overwrite loses thesis work
irrecoverably. (2) `lint.py` only checked the document total, though the config stores
per-section words_min/words_max. (3) `onboard`'s provisioning ignored the Windows
Microsoft-Store python stub and did not check for git. (4) The critic subagent had never
been exercised.

## Scope

In scope: onboard arms a local git safety net (init + first commit; backups/ fallback);
workspace CLAUDE.md snapshot rule for all phases; lint --min-words/--max-words (blocking)
wired into the check skill; Windows-aware provisioning (py launcher, Store stub, winget,
git check); critic exercised once with planted defects; version 0.1.3.
Out of scope: remote backups, pytest suite, store submission.

## Acceptance Criteria

- [x] onboard instructs git init + initial commit, plain-language framing, no upload.
- [x] Workspace CLAUDE.md carries the snapshot-before-overwrite rule.
- [x] lint exits 1 when a section is under --min-words or over --max-words; 0 in range.
- [x] Critic run on a draft with planted defects: all caught; stripping marks recovers
      the original text exactly (mark-only proven).
