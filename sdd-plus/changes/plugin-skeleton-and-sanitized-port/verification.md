# Verification

## Change

plugin-skeleton-and-sanitized-port

## Automated Checks

All run 2026-07-08 on Windows 11, Python 3.11, with scratchpad fixtures (fake academic
text; no real thesis data):

- [x] `python scripts/signals.py <fixture.md>` → scorecard + offenders printed
      (burstiness 0.358 correctly flagged below 0.55 target).
- [x] Gate PASS path: clean rephrase (figures/markers intact) → exit 0, "raíles ok".
- [x] Gate REJECT paths, each exit 1 with the rail named:
      figure changed (1.250→1.300 detected as lost/gained tokens);
      `[PENDIENTE]` dropped; banned term introduced (config-listed term detected).
- [x] Gate with NO config: banned-term fixture passes — proves the confidentiality list
      is per-project config, not built in.
- [x] `python scripts/lint.py` on dirty fixture → reports `[VERIFICAR]`, residual `[F#]`,
      5 cliché hits, em-dash count, confidentiality hit; exit 1 (blocking). Clean-ish
      fixture: exit 1 only due to `[PENDIENTE]` (correct), counters printed.
- [x] `python scripts/publish.py` with full config → .docx cover shows exactly the config
      values (university, degree, title, author, tutor role+name, academic year);
      AI declaration appended with config tool name; `[F#]` tags stripped.
- [x] Publish with EMPTY config → every cover line renders `[PENDIENTE: …]`; no default
      name appears anywhere (the original's hardcoded author/tutors are gone).
- [x] Sanitization sweep over the FULL working tree (tracked + untracked, .git excluded):
      - 8/8 original `BAD_TERMS` tokens: **zero matches**.
      - Personal/tutor name tokens: zero outside `BRIEF.md`/`LICENSE` (LICENSE =
        copyright line only, intentional).
      - `UDIT`/`SECPHO` (case-sensitive): only in BRIEF.md, PROJECT_CONTEXT.md and this
        change packet's governance docs — zero in product code (skills/, agents/,
        scripts/, config/, .claude-plugin/).
      - `openai`/`anthropic`/`API_KEY`: zero in product code (one hit = the spec delta
        describing this sweep).

## Manual Checks

- [x] Original scripts at `secpho_intelligence_system/TFM/agents/` opened read-only;
      no write operation was ever issued against that path.
- [x] `plugin.json`/`marketplace.json` mirror Drydock 0.3.0's field set (a plugin
      verified to load in this Claude Code installation).
- [x] Seven skills + critic agent reviewed against the port map: sanitized prompt rules
      carried over; UDIT-memoria specifics removed; critic constrained to mark-only.
- [ ] Plugin end-to-end load test (marketplace add + skill invocation) — deferred to the
      pilot session this afternoon; disclosed as the one untested surface.

## Documentation Updates

- [x] README carries the vision (written this change).
- [x] Project context created (PROJECT_CONTEXT.md).
- [x] Specs: three delta specs in this packet (plugin-structure,
      deterministic-guardrails, integrity-workflow).

## Result

PASS WITH OPEN QUESTIONS — all deterministic behavior proven offline; the only
undischarged item is the live plugin-install smoke test, scheduled for the pilot
session today.

Independent verifier (drydock:verifier, 2026-07-08): **PASS WITH OPEN QUESTIONS**.
Every reproducible claim reproduced with the verifier's own fixtures; sanitization
sweep independently confirmed clean (the go-public gate). Open items it left:
(a) tasks.md checkboxes — ticked; (b) live plugin-install smoke test — pending the
pilot session. Two fixture-count nits (cliché and doc-sweep counts differ between
fixture sets) noted as immaterial.
