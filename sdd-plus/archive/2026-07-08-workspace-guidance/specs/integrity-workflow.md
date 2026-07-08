# Spec Delta: workspace-guidance

Capability: integrity-workflow

## ADDED Requirements

### Requirement: Durable workspace guidance
The `onboard` skill SHALL install a standing `CLAUDE.md` in the student's workspace
(copied verbatim from the plugin's template) so that every new session self-orients from
the workspace files and re-applies the integrity rules without student commands.

#### Scenario: Fresh session in an onboarded workspace
- **WHEN** a new Claude Code session starts in a folder onboarded by TFMkit
- **THEN** the session reads the standing instructions, infers project state from
  `tfm.config.yaml` and the workspace folders, and tells the student where the project
  stands and what comes next
