# Plan

## Change

workspace-hardening

## Approach

Edit onboard (provisioning + safety net), workspace CLAUDE.md template (snapshot rule),
lint.py (section limit flags + blocking), check skill (pass limits from config). Exercise
the critic via a subagent running agents/critic.md verbatim on a planted-defect draft;
verify mark-only programmatically.

## Files Expected To Change

skills/onboard/SKILL.md · config/workspace-CLAUDE.template.md · scripts/lint.py ·
skills/check/SKILL.md · .claude-plugin/*.json (0.1.3)

## Risks

git may be absent and uninstallable on the pilot laptop — backups/ fallback documented.
Word counts include headings/markers (consistent with the existing total counter).

## Rollback

Revert the commit.
