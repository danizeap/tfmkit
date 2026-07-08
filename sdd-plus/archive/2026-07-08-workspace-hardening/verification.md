# Verification

## Change

workspace-hardening

## Automated Checks

- [x] lint --min-words 300 on a 223-word draft → "faltan 77", exit 1.
- [x] lint --max-words 200 on the same draft → "sobran 23", exit 1.
- [x] lint --min-words 100 --max-words 400 on a marker-free variant → exit 0.
- [x] Critic subagent (running agents/critic.md verbatim) on a draft with three planted
      defects (figure without [F#], banned cliché, no-reflection chronicle): all three
      marked (plus one legitimate extra finding); regex-stripping the marks reproduces
      the original text exactly → mark-only contract holds.
- [x] plugin.json/marketplace.json parse; 0.1.3. Sanitization sweep clean.

## Manual Checks

- [x] onboard provisioning reads correctly for a fresh Windows machine (py launcher
      first, Store-stub warning, winget ids for Python and Git).

## Result

PASS (LITE).
