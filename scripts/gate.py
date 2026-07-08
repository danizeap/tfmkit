"""SAFETY GATE — deterministic before/after judge for edit rounds. NO LLM, no network.

Claude Code runs the humanize/edit loop (tfmkit:check); this script only judges each round.
The rail is 'do not make it worse': it REFUSES any round that changes a numeric figure, drops a
[PENDIENTE], inserts editorial marks, adds an em-dash, or introduces a term from the project's
confidentiality list. On refusal the caller keeps the previous safe version.

The confidentiality list lives ONLY in the per-project tfm.config.yaml
(confidentiality.banned_terms) — TFMkit ships no built-in list, by design.

Usage:
  python scripts/gate.py <before.md> <after.md> [--config tfm.config.yaml]

Exit codes: 0 = round is safe (soft warnings may print) · 1 = round must be discarded.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Scope/emphasis words whose silent removal narrows meaning ("todos los datos" != "los datos").
EMPH = ["todos", "todo", "toda", "todas", "cada", "siempre", "nunca", "ningún", "ninguna",
        "solo", "sólo", "únicamente"]


def load_banned_terms(config_path: str | None) -> list[str]:
    """Per-project confidential terms from tfm.config.yaml; empty when unset."""
    if not config_path:
        return []
    try:
        import yaml
    except ImportError:
        raise SystemExit("Falta PyYAML para leer la configuración. Instala: pip install pyyaml")
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
    terms = (cfg.get("confidentiality") or {}).get("banned_terms") or []
    return [str(t) for t in terms if str(t).strip()]


def _figs(md: str) -> collections.Counter:
    """Multiset of numeric/figure tokens (counts, weights, dates, percentages).

    Internal separators only (0,44 · 23/03/2026 · v1.1); a trailing comma/period is sentence
    punctuation, not part of the number, so it is excluded — otherwise rephrasing flips '1' -> '1,'.
    """
    return collections.Counter(re.findall(r"\d+(?:[.,/]\d+)*", md))


def safety_gate(before: str, after: str, banned_terms: list[str] | None = None) -> list[str]:
    """Hard-rail violations that must discard the round. Empty list = safe."""
    issues = []
    lost = list((_figs(before) - _figs(after)).elements())
    gained = list((_figs(after) - _figs(before)).elements())
    if lost or gained:
        issues.append(f"cifras alteradas (faltan {lost or '—'}; nuevas {gained or '—'})")
    if after.count("[PENDIENTE") != before.count("[PENDIENTE"):
        issues.append("marcas [PENDIENTE] alteradas")
    new_marks = ((after.count("[VERIFICAR") + after.count("[AÑADIR REFLEXIÓN"))
                 - (before.count("[VERIFICAR") + before.count("[AÑADIR REFLEXIÓN")))
    if new_marks > 0:
        issues.append("insertó marcas editoriales/metacomentarios")
    if after.count("—") > before.count("—"):
        issues.append(f"añadió rayas em ({before.count('—')}→{after.count('—')})")
    hits = [b for b in (banned_terms or [])
            if b.lower() in after.lower() and b.lower() not in before.lower()]
    if hits:
        issues.append("confidencialidad NUEVA: " + ", ".join(hits))
    return issues


def soft_checks(before: str, after: str) -> list[str]:
    """Non-blocking warnings: things to eyeball, not hard violations."""
    warns = []
    def cnt(t):
        return sum(len(re.findall(r"\b" + w + r"\b", t.lower())) for w in EMPH)
    drop = cnt(before) - cnt(after)
    if drop > 0:
        warns.append(f"cayeron ~{drop} palabras de alcance/énfasis (todos/cada/solo…); "
                     "revisa que no se estreche el significado")
    return warns


def main():
    ap = argparse.ArgumentParser(
        description="Raíl de seguridad: compara antes/después de una ronda de edición. Sin LLM.")
    ap.add_argument("before", help=".md anterior (versión segura)")
    ap.add_argument("after", help=".md propuesto por la ronda de edición")
    ap.add_argument("--config", help="tfm.config.yaml (lista de confidencialidad del proyecto)")
    args = ap.parse_args()

    before = Path(args.before).read_text(encoding="utf-8")
    after = Path(args.after).read_text(encoding="utf-8")
    banned = load_banned_terms(args.config)

    issues = safety_gate(before, after, banned)
    if issues:
        print("✗ RONDA RECHAZADA (conserva la versión anterior):")
        for i in issues:
            print(f"  - {i}")
        sys.exit(1)

    print("✓ raíles ok — la ronda es segura")
    for w in soft_checks(before, after):
        print(f"  aviso: {w}")
    sys.exit(0)


if __name__ == "__main__":
    main()
