# Plan

## Change

workspace-guidance

## Approach

Add `config/workspace-CLAUDE.template.md` (standing instructions: orient from files,
workflow map, integrity rules, student profile). Reference it from the `onboard` skill's
project-structure step. Bump plugin version 0.1.0 → 0.1.1.

## Files Expected To Change

- config/workspace-CLAUDE.template.md (new)
- skills/onboard/SKILL.md
- .claude-plugin/plugin.json, .claude-plugin/marketplace.json (version)

## Risks

Minimal — documentation-layer change. Template must stay generic (sanitization rule
applies: nothing university-/person-specific).

## Rollback

Revert the commit; onboard falls back to not creating CLAUDE.md.
