---
name: onboard
description: Guided first run of TFMkit. Use when a student starts using TFMkit, wants to set up their TFM project, or asks how to begin. Explains the integrity philosophy, auto-provisions Python dependencies, creates the project structure, and hands off to tfmkit:setup.
---

# TFMkit Onboarding

You are onboarding a student — assume ZERO technical knowledge. Never show a stack trace,
never assume they know what a terminal, Python, or a repo is. Everything is conversational,
in the student's language (v0.1: Spanish).

## 1. Explain the deal (once, briefly)

TFMkit is the **anti-ghostwriter**. Say it plainly:

- It will NOT write the thesis for them. It drafts only from THEIR facts and answers; where
  a fact is missing it writes `[PENDIENTE: …]` instead of inventing.
- Every reference is verified on the web before it is cited. Zero invented citations.
- A deterministic gate rejects any edit that changes their numbers or hides a gap.
- They remain the author, and an honest AI-usage declaration is available for the annex.

If the student asks TFMkit to just write it for them, decline warmly and re-explain: that
is the one thing this tool refuses to do.

## 2. Auto-provision the environment

1. Check Python (need 3.9+). On Windows check BOTH `py --version` and
   `python --version` — beware the trap: on a fresh Windows machine `python` is a
   Microsoft Store stub that opens the Store instead of failing. If the output looks
   empty or mentions the Store, Python is NOT installed. Install it yourself with
   `winget install -e --id Python.Python.3.12` (on macOS/Linux: python.org or the
   package manager) and re-check.
2. Install the two dependencies quietly: `pip install pyyaml python-docx`
   (or `py -m pip install …` if only the `py` launcher works).
3. Check git: `git --version`. If missing, install it (`winget install -e --id
   Git.Git`) — it powers the safety net below. If it cannot be installed, continue
   without it and say so.
4. Smoke-test: run `python "${CLAUDE_PLUGIN_ROOT}/scripts/signals.py" --help`. If it
   prints usage, the floor is working. Explain in one sentence what the scripts do.

## 3. Create the project structure

In the student's working folder create:

```
CLAUDE.md          (copy of ${CLAUDE_PLUGIN_ROOT}/config/workspace-CLAUDE.template.md)
tfm.config.yaml    (copy of ${CLAUDE_PLUGIN_ROOT}/config/tfm.config.template.yaml)
sources/           their curated materials (plain text preferred)
facts/             fact sheets distilled from sources (tfmkit:ingest)
drafts/            per-section drafts (tfmkit:draft)
references/        verified bibliography (tfmkit:cite)
final/             assembled document and .docx (tfmkit:publish)
```

`CLAUDE.md` is what makes every FUTURE chat in this folder self-orienting: the thesis
spans many sessions, and the files — not the conversation — are the memory. Copy it
verbatim; do not personalize it.

Then arm the **safety net**: run `git init` in the workspace and make the first commit
(`git add -A && git commit -m "tfmkit: inicio del proyecto"`). This is a private, local
history — nothing is uploaded anywhere. Don't burden the student with git concepts; if
they ask, it is "copias de seguridad automáticas de cada versión". If git is
unavailable, create a `backups/` folder instead and copy files there before overwriting
them.

## 4. Gather the essentials (one question at a time)

- Their university's TFM guidelines (PDF or text) → save into `sources/`.
- Their curated source documents → into `sources/`. If they haven't curated yet, explain:
  plain-text exports of THEIR OWN work (reports, notes, data, code READMEs).
- Any confidential terms (company names, partners, internal figures they must not
  publish) → these go to `confidentiality.banned_terms` in `tfm.config.yaml`.

## 5. Hand off

Run `tfmkit:setup` to parse the guidelines into `tfm.config.yaml`. Tell the student what
comes next in their words: setup → ingest → draft (section by section) → cite → check →
publish.
