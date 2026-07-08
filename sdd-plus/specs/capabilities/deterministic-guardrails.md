# Capability: deterministic-guardrails

Status: active. Last synced from change: workspace-hardening (2026-07-08).

## Requirements

### Requirement: Style-signal analysis
`scripts/signals.py` SHALL deterministically compute, for a Markdown document's flowing
prose: burstiness (sd/mean sentence length), short/long sentence percentages, TTR,
repeated 3/4-grams, sentence-opener counts, connector densities, and em-dash count — with
no network access.

#### Scenario: Scorecard output
- **WHEN** `python scripts/signals.py <file.md>` runs on a document with prose
- **THEN** it prints a scorecard and an offenders list naming the concrete weak signals

### Requirement: Safety gate rejects fact-breaking edits
`scripts/gate.py` SHALL compare a before and an after version and exit non-zero when any
hard rail breaks: a numeric figure token lost or gained, a `[PENDIENTE]` marker count
change, new `[VERIFICAR]`/`[AÑADIR REFLEXIÓN]` marks, an increase in em-dashes, or the
appearance of a term from the project's `confidentiality.banned_terms` config list.

#### Scenario: Figure alteration rejected
- **WHEN** the after version drops or changes any number present in the before version
- **THEN** the gate exits non-zero and names the lost/gained figure tokens

#### Scenario: Confidential term rejected
- **WHEN** the config lists a banned term and the after version introduces it
- **THEN** the gate exits non-zero and names the term

#### Scenario: Clean edit passes
- **WHEN** the after version rephrases prose without touching figures, markers, em-dashes,
  or banned terms
- **THEN** the gate exits zero (soft warnings, e.g. lost emphasis words, do not block)

### Requirement: Confidentiality list is config-only
The gate and lint SHALL read confidential terms exclusively from the per-project config;
the codebase SHALL ship no built-in confidential term list.

#### Scenario: No hardcoded terms
- **WHEN** product sources are searched for the original private repo's `BAD_TERMS` entries
- **THEN** zero matches are found

### Requirement: Offline lint and counters
`scripts/lint.py` SHALL report unresolved `[PENDIENTE]`/`[VERIFICAR]`/`[AÑADIR REFLEXIÓN]`
markers, residual `[F#]` tags, AI-cliché hits (generic ES/EN list), em-dash count,
flat-rhythm paragraphs, and word/character counts checked against config limits.
Additionally, the lint SHALL accept per-section word limits (`--min-words`,
`--max-words`) and SHALL exit non-zero when the document falls outside them.

#### Scenario: Marker report
- **WHEN** a document containing `[PENDIENTE: x]` and a cliché is linted
- **THEN** both are reported with counts

#### Scenario: Section under minimum
- **WHEN** a section draft has fewer words than the configured minimum
- **THEN** the lint reports how many words are missing and exits non-zero

### Requirement: Config-driven typesetter
`scripts/publish.py` SHALL build a .docx whose cover (university, degree, title, author,
tutors, academic year) comes only from config values, SHALL strip `[F#]` tags from the
body, and SHALL append a generalized AI-usage declaration when enabled — with no personal
or institutional defaults hardcoded. Additionally, the typesetter SHALL style heading
levels 1-3 with the configured font (black, sized relative to the base size), SHALL place
a page-number field in the footer of every page except the cover, and SHALL insert a
paginated table-of-contents field after the cover when `typography.include_toc` is
enabled (default true).

#### Scenario: Missing config value
- **WHEN** a cover field is absent from the config
- **THEN** the output shows a `[PENDIENTE: …]` placeholder, never a default name

#### Scenario: Compliant deliverable
- **WHEN** a document is published with a configured font
- **THEN** headings and body share that font, pages after the cover are numbered, and a
  TOC field is present for Word to paginate
