# TFMkit

**The anti-ghostwriter.** An open-source Claude Code plugin that helps a student write their
TFM (Spanish master's thesis) **with integrity** — it never writes the thesis *for* them.

TFMkit interviews the author, distills **their** materials into traceable fact sheets, drafts
only from those facts, verifies every citation on the web before it is cited, hunts AI-text
tells, checks the university's own guidelines, and typesets the deliverable. The student
remains the author.

## How it works

Claude Code **is** the model — TFMkit ships **zero API keys**. The plugin is three layers:

1. **Skills** that govern Claude through the workflow:
   `onboard → setup → ingest → draft → cite → check → publish`
2. **A critic subagent** in a fresh context that only *marks* problems — it never rewrites.
3. **Deterministic Python scripts** (no LLM) as the floor: style-signal analysis
   (burstiness, openers, n-grams, connectors), lint and counters, a safety gate that rejects
   any edit round that alters a figure or drops a `[PENDIENTE]` marker, and the docx/PDF
   typesetter.

Everything university- or project-specific — section structure, word limits, typography,
margins, and the per-project **confidentiality list** — lives in `tfm.config.yaml`. Nothing
is hardcoded.

## Integrity principles (non-negotiable)

1. Facts come from the author (curated docs + interview). A gap is `[PENDIENTE: …]`, never invention.
2. No reference goes in unverified online. Zero fabricated citations.
3. The critic marks; it never rewrites. The deterministic gate rejects rounds that alter figures or markers.
4. Confidentiality by design: a per-project banned-terms list, enforced by the lint.
5. Honest disclosure: an AI-usage declaration template is provided.
6. The student is the author. TFMkit is governed assistance, not a ghostwriter.

## Status

Pre-release (v0.1 in development). v0.1 targets **Spanish-language TFMs**; the style tells and
lints are Spanish-calibrated. Code, docs and process are in English.

## License

[MIT](LICENSE)
