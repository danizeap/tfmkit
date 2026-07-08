# Spec Delta: pilot-readiness

Capability: deterministic-guardrails

## MODIFIED Requirements

### Requirement: Config-driven typesetter
Additionally, the typesetter SHALL style heading levels 1-3 with the configured font
(black, sized relative to the base size), SHALL place a page-number field in the footer
of every page except the cover, and SHALL insert a paginated table-of-contents field
after the cover when `typography.include_toc` is enabled (default true).

#### Scenario: Compliant deliverable
- **WHEN** a document is published with a configured font
- **THEN** headings and body share that font, pages after the cover are numbered, and a
  TOC field is present for Word to paginate
