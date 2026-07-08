"""Local AI-detection-style signal analysis for the TFMkit pipeline. NO data leaves the machine.

Measures the proxy signals that real detectors lean on — burstiness (sentence-length variation),
sentence-length distribution, sentence-opening diversity, repeated n-grams, connector density,
lexical diversity (TTR) and em-dash count — and surfaces the concrete 'offenders' the humanize pass
should attack. It is a PROXY for proprietary detectors, not a replacement.

Deterministic: no LLM, no network. Claude Code (the model) reads this scorecard and does the
rewriting itself, then scripts/gate.py judges the result.

Usage:
  python scripts/signals.py <document.md> [--config tfm.config.yaml] [--json]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Indicative human-band threshold (proxy target); overridable via config style.target_burstiness.
TARGET_BURSTINESS = 0.55

_ARTICLES = {"el", "la", "los", "las"}
_CONNECTORS = ["además", "asimismo", "por tanto", "por ello", "en conjunto", "sin embargo",
               "no obstante", "es decir", "en definitiva", "cabe", "por consiguiente", "fiel"]


def prose_of(md: str) -> str:
    """Flowing prose only: drop code blocks, tables, headings, bullets, numbered lists and data sheets."""
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    keep = [s for s in (ln.strip() for ln in md.splitlines())
            if s and not re.match(r"^(#|\||>|[-*]\s|\d+\.\s)", s)]
    t = " ".join(keep)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)  # [text](url) -> text
    t = re.sub(r"[*`#]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def _sentences(text: str):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]


def analyze(md: str) -> dict:
    text = prose_of(md)
    sents = _sentences(text)
    lens = [n for n in (len(re.findall(r"\w+", s)) for s in sents) if n > 0]
    words = re.findall(r"\w+", text.lower())
    if not lens or not words:
        return {}
    mean = statistics.mean(lens)
    sd = statistics.pstdev(lens)

    def ngr(n):
        c = collections.Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))
        return [(" ".join(g), v) for g, v in c.most_common(12) if v >= 3]

    openers = collections.Counter(s.split()[0].lower() for s in sents if s.split())
    conn = {c: len(re.findall(r"\b" + re.escape(c) + r"\b", text.lower())) for c in _CONNECTORS}
    return {
        "n_sents": len(sents), "n_words": len(words),
        "mean_len": round(mean, 1), "sd_len": round(sd, 1),
        "burstiness": round(sd / mean, 3),
        "pct_short": round(sum(1 for l in lens if l <= 8) / len(lens) * 100, 1),
        "pct_long": round(sum(1 for l in lens if l >= 30) / len(lens) * 100, 1),
        "ttr": round(len(set(words)) / len(words), 3),
        "rep3": ngr(3), "rep4": ngr(4),
        "top_openers": openers.most_common(6),
        "connectors": {k: v for k, v in conn.items() if v},
        "emdashes": md.count("—"),
    }


def offenders(d: dict, target_burstiness: float = TARGET_BURSTINESS) -> str:
    """Concrete weak-signal checklist the humanize pass must attack."""
    if not d:
        return "- (sin prosa analizable)"
    out = []
    if d["burstiness"] < target_burstiness:
        out.append(f"- BURSTINESS BAJA ({d['burstiness']}, objetivo >= {target_burstiness}): intercala más "
                   f"frases CORTAS y rotundas entre las largas (hoy solo {d['pct_short']}% son cortas).")
    rep_open = [f"«{w}» ({n}x)" for w, n in d["top_openers"]
                if (n >= 5 and w not in _ARTICLES) or (w in _ARTICLES and n >= 12)]
    if rep_open:
        out.append("- APERTURAS REPETIDAS (varía el comienzo de esas frases): " + ", ".join(rep_open) + ".")
    if d["rep4"]:
        out.append("- 4-GRAMAS REPETIDOS (rómpelos salvo que sean términos técnicos imprescindibles): "
                   + "; ".join(f"\"{g}\" ({n}x)" for g, n in d["rep4"]))
    over = [f"{k} ({v}x)" for k, v in d["connectors"].items() if v >= 3]
    if over:
        out.append("- CONECTORES ABUSADOS (redúcelos): " + ", ".join(over))
    if d["emdashes"]:
        out.append(f"- RAYAS EM: {d['emdashes']} en el texto -> deben quedar 0.")
    return "\n".join(out) if out else "- (sin señales débiles claras; solo pulido fino de ritmo)"


def scorecard(d: dict) -> str:
    if not d:
        return "(sin prosa analizable)"
    return (f"frases {d['n_sents']} · media {d['mean_len']} (sd {d['sd_len']}) · "
            f"BURSTINESS {d['burstiness']} · cortas {d['pct_short']}% · largas {d['pct_long']}% · "
            f"TTR {d['ttr']} · rayas {d['emdashes']}")


def _target_from_config(path: str | None) -> float:
    if not path:
        return TARGET_BURSTINESS
    try:
        import yaml
        cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return float((cfg.get("style") or {}).get("target_burstiness") or TARGET_BURSTINESS)
    except Exception:
        return TARGET_BURSTINESS


def main():
    ap = argparse.ArgumentParser(description="Señales de estilo (proxy anti-detector) de un .md. Sin red, sin LLM.")
    ap.add_argument("infile", help="documento .md a analizar")
    ap.add_argument("--config", help="tfm.config.yaml (para style.target_burstiness)")
    ap.add_argument("--json", action="store_true", help="salida JSON completa")
    args = ap.parse_args()

    md = Path(args.infile).read_text(encoding="utf-8")
    d = analyze(md)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return
    print("SCORECARD:", scorecard(d))
    print("\nSEÑALES DÉBILES:")
    print(offenders(d, _target_from_config(args.config)))


if __name__ == "__main__":
    main()
