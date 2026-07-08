"""LINT — offline integrity and style report for a TFM Markdown document. NO LLM, no network.

Surfaces everything the author must resolve before submission: unresolved [PENDIENTE] gaps,
[VERIFICAR] claims, [AÑADIR REFLEXIÓN] marks, residual [F#] traceability tags, generic AI clichés
(Spanish/English), em-dashes, flat-rhythm paragraphs, word/character counters against the config
limits, and any hit from the project's confidentiality list (config-only; TFMkit ships none).

Usage:
  python scripts/lint.py <document.md> [--config tfm.config.yaml]

Exit codes: 0 = clean · 1 = blocking findings (unresolved markers, confidentiality hits,
limits exceeded).
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Generic AI-tell clichés (calibrated on real Spanish academic drafts). Not confidential.
CLICHES = [
    # ES
    "cabe destacar", "cabe señalar", "es importante señalar", "es importante destacar",
    "en un mundo donde", "en la era actual", "en la sociedad actual", "juega un papel fundamental",
    "juega un papel crucial", "en conclusión", "en resumen", "sin lugar a dudas", "no solo",
    "panorama", "sinergia", "robusto", "transformador", "fomentar", "subrayar",
    # EN
    "delve", "leverage", "crucial", "pivotal", "testament", "underscore", "seamless", "robust",
    "it is worth noting", "in today's world",
]


def load_config(config_path: str | None) -> dict:
    if not config_path:
        return {}
    try:
        import yaml
    except ImportError:
        raise SystemExit("Falta PyYAML para leer la configuración. Instala: pip install pyyaml")
    return yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}


def lint(md: str, cfg: dict | None = None, min_words: int | None = None,
         max_words: int | None = None) -> dict:
    cfg = cfg or {}
    low = md.lower()
    paras = [p for p in md.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    flat = []
    for para in paras:
        sents = [s for s in re.split(r"[.!?]+", para) if s.strip()]
        lens = [len(s.split()) for s in sents]
        if len(lens) >= 3 and statistics.pstdev(lens) < 4:
            flat.append(" ".join(para.split())[:70])

    banned = [str(t) for t in ((cfg.get("confidentiality") or {}).get("banned_terms") or [])
              if str(t).strip()]
    words_total = len(re.findall(r"\w+", md))
    limits = cfg.get("limits") or {}

    return {
        "pendientes": re.findall(r"\[PENDIENTE:[^\]]*\]", md),
        "verificar": re.findall(r"\[VERIFICAR:[^\]]*\]", md),
        "reflexion": re.findall(r"\[AÑADIR REFLEXIÓN:[^\]]*\]", md),
        "ftags": re.findall(r"\[F\d+\]", md),
        "cliches": sorted({c for c in CLICHES if c in low}),
        "rayas": md.count("—"),
        "ritmo_plano": flat,
        "confidencialidad": sorted({b for b in banned if b.lower() in low}),
        "palabras": words_total,
        "caracteres": len(md),
        "exceso_palabras": (words_total - limits["total_words_max"]
                            if limits.get("total_words_max") else 0),
        # Per-section limits (drafts are one file per section): pass the section's
        # words_min/words_max from tfm.config.yaml via --min-words/--max-words.
        "defecto_seccion": (min_words - words_total
                            if min_words and words_total < min_words else 0),
        "exceso_seccion": (words_total - max_words
                           if max_words and words_total > max_words else 0),
    }


def print_report(rep: dict) -> None:
    print("=== LINT ===")
    print(f"  [PENDIENTE] sin resolver : {len(rep['pendientes'])}")
    for p in rep["pendientes"][:25]:
        print(f"      - {p}")
    print(f"  [VERIFICAR] afirmaciones : {len(rep['verificar'])}")
    print(f"  [AÑADIR REFLEXIÓN]       : {len(rep['reflexion'])}")
    print(f"  marcas [F#] sin retirar  : {len(rep['ftags'])}")
    print(f"  muletillas de IA detectadas: {', '.join(rep['cliches']) or 'ninguna'}")
    print(f"  rayas (—) en el texto    : {rep['rayas']}")
    print(f"  párrafos de ritmo plano  : {len(rep['ritmo_plano'])}")
    for p in rep["ritmo_plano"][:10]:
        print(f"      - {p}…")
    print(f"  palabras / caracteres    : {rep['palabras']} / {rep['caracteres']}")
    if rep["exceso_palabras"] > 0:
        print(f"  ⚠ LÍMITE SUPERADO: {rep['exceso_palabras']} palabras por encima del máximo configurado")
    if rep["exceso_seccion"] > 0:
        print(f"  ⚠ LÍMITE DE SECCIÓN SUPERADO: sobran {rep['exceso_seccion']} palabras")
    if rep["defecto_seccion"] > 0:
        print(f"  ⚠ SECCIÓN CORTA: faltan {rep['defecto_seccion']} palabras para el mínimo")
    if rep["confidencialidad"]:
        print(f"  ✗ CONFIDENCIALIDAD: términos vetados presentes: {', '.join(rep['confidencialidad'])}")


def is_blocking(rep: dict) -> bool:
    return bool(rep["pendientes"] or rep["verificar"] or rep["reflexion"]
                or rep["confidencialidad"] or rep["exceso_palabras"] > 0
                or rep["exceso_seccion"] > 0 or rep["defecto_seccion"] > 0)


def main():
    ap = argparse.ArgumentParser(description="Lint offline de integridad y estilo. Sin LLM, sin red.")
    ap.add_argument("infile", help="documento .md")
    ap.add_argument("--config", help="tfm.config.yaml (límites y lista de confidencialidad)")
    ap.add_argument("--min-words", type=int, help="mínimo de palabras de ESTA sección (de la guía)")
    ap.add_argument("--max-words", type=int, help="máximo de palabras de ESTA sección (de la guía)")
    args = ap.parse_args()

    md = Path(args.infile).read_text(encoding="utf-8")
    rep = lint(md, load_config(args.config), args.min_words, args.max_words)
    print_report(rep)
    sys.exit(1 if is_blocking(rep) else 0)


if __name__ == "__main__":
    main()
