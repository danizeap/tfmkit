# Capability: integrity-workflow

Status: active. Last synced from change: workspace-hardening (2026-07-08).

## Requirements

### Requirement: Fail-closed drafting
The `draft` skill SHALL instruct Claude to draft exclusively from the project's fact
sheets and interview answers, inserting `[PENDIENTE: <what is missing>]` for any gap and
tagging fact-bearing sentences with `[F#]` identifiers — never filling gaps with plausible
content.

#### Scenario: Missing fact
- **WHEN** a sentence needs a datum absent from the fact sheets
- **THEN** the draft contains a `[PENDIENTE]` marker instead of an invented value

### Requirement: Interview before prose
The `draft` skill SHALL run an interview (3–6 concrete, decision/obstacle/figure/learning
questions per section) before drafting, and record answers into the fact sheet with
provenance.

#### Scenario: Section start
- **WHEN** the author asks to draft a section with insufficient facts
- **THEN** Claude asks concrete questions first and drafts only after answers (or gaps
  marked `[PENDIENTE]`)

### Requirement: Web-verified citations only
The `cite` skill SHALL require every reference to be verified online (authors, year,
venue) via WebSearch before it enters the text or bibliography, formatted APA 7; a
reference that cannot be verified SHALL be marked and excluded.

#### Scenario: Unverifiable reference
- **WHEN** a candidate source cannot be confirmed to exist
- **THEN** it is not cited and the author is told why

### Requirement: Critic marks, never rewrites
The `critic` subagent SHALL review drafts in a fresh context and only insert
`[VERIFICAR]`/`[AÑADIR REFLEXIÓN]` marks with reasons; it SHALL NOT rewrite prose.

#### Scenario: Unsupported claim
- **WHEN** the critic finds a concrete claim without `[F#]` backing
- **THEN** it adds `[VERIFICAR: …]` beside it and changes nothing else

### Requirement: Gate-checked edit rounds
The `check` skill SHALL run every humanize/edit round through `scripts/gate.py` and
discard any round the gate rejects, keeping the last safe version.

#### Scenario: Rejected round
- **WHEN** an edit round alters a figure or drops a `[PENDIENTE]`
- **THEN** the round is discarded and the reason is reported to the author in plain terms

### Requirement: Durable workspace guidance
The `onboard` skill SHALL install a standing `CLAUDE.md` in the student's workspace
(copied verbatim from the plugin's template) so that every new session self-orients from
the workspace files and re-applies the integrity rules without student commands.

#### Scenario: Fresh session in an onboarded workspace
- **WHEN** a new Claude Code session starts in a folder onboarded by TFMkit
- **THEN** the session reads the standing instructions, infers project state from
  `tfm.config.yaml` and the workspace folders, and tells the student where the project
  stands and what comes next

### Requirement: Workspace safety net
The `onboard` skill SHALL initialize a local git repository in the student's workspace
(with a plain-language explanation and no remote), and every session SHALL snapshot the
workspace after file-changing steps and before overwriting any draft; where git is
unavailable, timestamped copies in `backups/` substitute.

#### Scenario: Draft about to be overwritten
- **WHEN** an edit round is adopted over an existing draft
- **THEN** the prior version is recoverable from the workspace history
