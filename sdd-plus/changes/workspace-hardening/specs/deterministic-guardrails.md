# Spec Delta: workspace-hardening

Capability: deterministic-guardrails

## MODIFIED Requirements

### Requirement: Offline lint and counters
Additionally, the lint SHALL accept per-section word limits (`--min-words`,
`--max-words`) and SHALL exit non-zero when the document falls outside them.

#### Scenario: Section under minimum
- **WHEN** a section draft has fewer words than the configured minimum
- **THEN** the lint reports how many words are missing and exits non-zero
