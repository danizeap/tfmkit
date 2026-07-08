# Capability: plugin-structure

Status: active. Last synced from change: plugin-skeleton-and-sanitized-port (2026-07-08).

## Requirements

### Requirement: Installable Claude Code plugin
The system SHALL be a valid Claude Code plugin rooted at the repository top level, with a
`.claude-plugin/plugin.json` manifest and a `.claude-plugin/marketplace.json` whose single
plugin entry uses `source: "./"`.

#### Scenario: Plugin discovery
- **WHEN** the repository is added as a marketplace and the plugin installed
- **THEN** Claude Code discovers seven skills (`onboard`, `setup`, `ingest`, `draft`,
  `cite`, `check`, `publish`) under `skills/` and one subagent (`critic`) under `agents/`

### Requirement: Zero API keys in the product
The product SHALL contain no LLM API client, no API-key reference, and no network-calling
code except what Claude Code itself provides (e.g. WebSearch used by skills).

#### Scenario: Static sweep
- **WHEN** the repository is searched for `openai`, `anthropic` imports or `API_KEY`
  variables in product code
- **THEN** zero matches are found

### Requirement: Project-specific data lives only in config
Everything university-, project-, or person-specific (cover data, section registry,
limits, typography, confidentiality terms, AI-disclosure tool name) SHALL live in
`tfm.config.yaml`, created per project from `config/tfm.config.template.yaml`; the
template SHALL ship with an empty `confidentiality.banned_terms` list and no real names.

#### Scenario: Template is clean
- **WHEN** the config template is inspected
- **THEN** it contains placeholders only — no real university, person, company, or figure
