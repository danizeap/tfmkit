# Spec Delta: workspace-hardening

Capability: integrity-workflow

## ADDED Requirements

### Requirement: Workspace safety net
The `onboard` skill SHALL initialize a local git repository in the student's workspace
(with a plain-language explanation and no remote), and every session SHALL snapshot the
workspace after file-changing steps and before overwriting any draft; where git is
unavailable, timestamped copies in `backups/` substitute.

#### Scenario: Draft about to be overwritten
- **WHEN** an edit round is adopted over an existing draft
- **THEN** the prior version is recoverable from the workspace history
