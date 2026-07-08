"""Signals is the measurement layer; it must be deterministic and prose-only."""
import signals

PROSE = (
    "# Título\n\n"
    "La primera frase del documento es bastante larga y contiene muchas palabras "
    "encadenadas sin pausa aparente. Corta. Después llega otra frase de longitud "
    "media que equilibra el conjunto. Otra corta. Y una final que vuelve a estirarse "
    "para dar variedad al ritmo del párrafo completo.\n"
)


def test_analyze_reports_core_metrics():
    d = signals.analyze(PROSE)
    assert d["n_sents"] == 5
    assert 0 < d["burstiness"]
    assert d["emdashes"] == 0
    assert 0 < d["ttr"] <= 1


def test_prose_of_strips_structure():
    md = "# H\n\n| a | b |\n|---|---|\n\n```code aquí```\n\n- bullet\n\nSolo esta frase queda.\n"
    assert signals.prose_of(md) == "Solo esta frase queda."


def test_empty_document_is_safe():
    assert signals.analyze("") == {}
    assert "sin prosa" in signals.scorecard({})
    assert "sin prosa" in signals.offenders({})


def test_offenders_flags_low_burstiness():
    flat = "# T\n\n" + " ".join(
        f"Esta frase número {i} tiene exactamente las mismas palabras contadas." for i in range(8)
    )
    d = signals.analyze(flat)
    out = signals.offenders(d, target_burstiness=0.55)
    assert "BURSTINESS BAJA" in out


def test_emdash_counted_and_flagged():
    d = signals.analyze(PROSE.replace("Corta.", "Corta — sí."))
    assert d["emdashes"] == 1
    assert "RAYAS EM" in signals.offenders(d)
