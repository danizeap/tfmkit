# Brief

## Change

workspace-guidance

## What this means for your product

After this change, your friend can close his laptop, come back tomorrow, open any new
chat in his thesis folder, and Claude picks up exactly where he left off — no commands,
no memory required from him.

## User Need

The pilot will work across many sessions over ~10 days. A new chat knows nothing about
the project unless the folder itself carries standing instructions.

## Problem

`onboard` creates the workspace but leaves no CLAUDE.md, so every fresh session starts
blind: no phase awareness, no integrity rules in context, no student profile.

## Scope

In scope: a workspace CLAUDE.md template shipped in `config/`; `onboard` copies it into
the student's folder; plugin version bump to 0.1.1.
Out of scope: any change to the other skills, scripts, or config schema.

## Acceptance Criteria

- [x] `config/workspace-CLAUDE.template.md` ships with orientation procedure, workflow
      map, integrity rules, and student profile — nothing project- or person-specific.
- [x] `onboard` instructs copying it verbatim as `CLAUDE.md` in the workspace.
- [x] Version 0.1.1 in plugin.json and marketplace.json.
