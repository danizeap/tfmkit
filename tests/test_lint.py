"""Lint surfaces what the author must resolve; blocking semantics are the contract."""
import lint

CLEAN = (
    "# Sección\n\n"
    "El estudio abarcó 4.820 registros. Se aplicó validación temporal con un año de "
    "prueba. Los resultados quedaron documentados con detalle suficiente.\n"
)
DIRTY = (
    "# Sección\n\n"
    "Cabe destacar que el panorama es robusto — transformador incluso. [F2]\n\n"
    "[PENDIENTE: dato] y además [VERIFICAR: afirmación sin respaldo].\n"
)


def test_clean_doc_not_blocking():
    rep = lint.lint(CLEAN)
    assert not lint.is_blocking(rep)
    assert rep["cliches"] == [] and rep["rayas"] == 0


def test_markers_detected_and_blocking():
    rep = lint.lint(DIRTY)
    assert len(rep["pendientes"]) == 1
    assert len(rep["verificar"]) == 1
    assert lint.is_blocking(rep)


def test_cliches_and_emdash_reported():
    rep = lint.lint(DIRTY)
    assert "cabe destacar" in rep["cliches"] and "panorama" in rep["cliches"]
    assert rep["rayas"] == 1


def test_ftags_reported_but_not_blocking():
    rep = lint.lint("# S\n\nDato con respaldo [F3]. Frase corta. Otra más aquí.\n")
    assert len(rep["ftags"]) == 1
    assert not lint.is_blocking(rep)


def test_confidentiality_from_config_blocks():
    cfg = {"confidentiality": {"banned_terms": ["AcmeSecreta"]}}
    rep = lint.lint(CLEAN + "\nColaboró AcmeSecreta.\n", cfg)
    assert rep["confidencialidad"] == ["AcmeSecreta"]
    assert lint.is_blocking(rep)


def test_total_limit_from_config():
    cfg = {"limits": {"total_words_max": 5}}
    rep = lint.lint(CLEAN, cfg)
    assert rep["exceso_palabras"] > 0 and lint.is_blocking(rep)


def test_section_min_words_blocks():
    rep = lint.lint(CLEAN, min_words=1000)
    assert rep["defecto_seccion"] > 0 and lint.is_blocking(rep)


def test_section_max_words_blocks():
    rep = lint.lint(CLEAN, max_words=5)
    assert rep["exceso_seccion"] > 0 and lint.is_blocking(rep)


def test_section_limits_in_range_pass():
    rep = lint.lint(CLEAN, min_words=5, max_words=1000)
    assert rep["defecto_seccion"] == 0 and rep["exceso_seccion"] == 0
    assert not lint.is_blocking(rep)
