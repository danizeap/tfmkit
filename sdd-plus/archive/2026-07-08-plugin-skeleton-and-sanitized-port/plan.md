# Plan

## Change

plugin-skeleton-and-sanitized-port

## Approach

Follow Drydock's repo convention: the repo IS the plugin (manifest at root), governance
(`sdd-plus/`) coexists alongside. Port the deterministic layer from the private SECPHO
agents with sanitization applied at the source line, never after the fact.

1. **Plugin skeleton**
   - `.claude-plugin/plugin.json` — name `tfmkit`, MIT, author danizeap (mirrors Drydock's
     manifest shape).
   - `.claude-plugin/marketplace.json` — single plugin, `source: "./"`.
   - `skills/{onboard,setup,ingest,draft,cite,check,publish}/SKILL.md` — each a governed
     procedure for Claude (no LLM of their own). `draft`/`check` carry the sanitized
     writer/editor rules from the original prompts; `cite` encodes web-verified APA 7;
     `ingest` encodes fact sheets with per-fact provenance + `[PENDIENTE]` gaps.
   - `agents/critic.md` — external critic subagent: marks `[VERIFICAR]`/`[AÑADIR
     REFLEXIÓN]`, never rewrites (sanitized `editor_system.md`).
   - `config/tfm.config.template.yaml` — everything project-specific: cover data
     (title/author/university/degree/year/tutors), section registry (generic defaults,
     filled by `setup` from the user's guidelines), limits, typography, style targets,
     `confidentiality.banned_terms: []`, AI-disclosure settings.
2. **Sanitized deterministic scripts** (`scripts/`, stdlib + PyYAML + python-docx)
   - `signals.py` ← original `signals.py` (clean; ported nearly as-is, CLI added).
   - `gate.py` ← `editor.py` minus the LLM loop (Claude runs the loop): figure multiset
     diff, `[PENDIENTE]`/editorial-marker rails, em-dash rail, emphasis-word soft check;
     **confidential terms come only from `--config`** (the original `BAD_TERMS` constant
     is NOT copied — the list ships empty). Exit code 1 on any hard-rail violation.
   - `lint.py` ← `publisher.py` lint half: markers, `[F#]` tags, ES/EN cliché list
     (generic tells only — no confidential terms), em-dashes, flat-rhythm paragraphs,
     word/char counters checked against config limits.
   - `publish.py` ← `publisher.py` docx half: cover built exclusively from config values
     (missing value → `[PENDIENTE: …]` placeholder, never a hardcoded default);
     generalized AI-disclosure template (tool name from config).
   - No `common.py` port: it is the OpenAI client — dropped entirely.
3. **Verification**: scratchpad fixtures (fake before/after md) prove signals/lint run,
   gate rejects each rail violation and passes a clean edit, publish produces a docx.
   Sanitization proven by `git grep` sweep for every forbidden token (checked against the
   original lists read from the SECPHO repo, which stays untouched).
4. **Verifier subagent review** (FULL mode), then commit.

## Files Expected To Change

All new; no existing files modified except `.gitignore` if needed:

- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- `skills/onboard/SKILL.md`, `skills/setup/SKILL.md`, `skills/ingest/SKILL.md`,
  `skills/draft/SKILL.md`, `skills/cite/SKILL.md`, `skills/check/SKILL.md`,
  `skills/publish/SKILL.md`
- `agents/critic.md`
- `scripts/signals.py`, `scripts/gate.py`, `scripts/lint.py`, `scripts/publish.py`
- `config/tfm.config.template.yaml`
- Change-packet artifacts under `sdd-plus/changes/plugin-skeleton-and-sanitized-port/`

## Risks

- **Confidential leakage** (highest): a `BAD_TERMS` token, personal name, or UDIT string
  slips into the port. Mitigation: sanitize at write time + explicit grep sweep as an
  acceptance gate + verifier check before commit.
- Plugin manifest fields drift from current Claude Code spec → plugin fails to load.
  Mitigation: mirror Drydock 0.3.0's working manifest.
- PyYAML/python-docx missing on the pilot's machine → `onboard` skill auto-provisions;
  scripts degrade with a clear Spanish install hint, never a stack trace.
- Deadline pressure tempts scope growth (full onboarding UX today). Mitigation: stop
  condition — anything beyond skeleton+port is a new bounded change.

## Rollback

Single revertable commit on `main`; no external side effects, no data migrations. The
original SECPHO scripts are untouched, so reverting the commit fully restores the
pre-change world.
