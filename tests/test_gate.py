"""The safety gate is the integrity floor: every rail must reject, and only rails reject."""
import gate

BEFORE = (
    "# Sección\n\n"
    "El sistema procesó 1.250 documentos en 3 fases durante 2025. La mejora fue del "
    "12,5% sobre la línea base. [PENDIENTE: fecha exacta]\n\n"
    "Se evaluaron todas las alternativas. Cada iteración duró 2 semanas.\n"
)


def test_clean_rephrase_passes():
    after = BEFORE.replace("El sistema procesó", "Durante el estudio, el sistema procesó")
    assert gate.safety_gate(BEFORE, after) == []


def test_changed_figure_rejected():
    after = BEFORE.replace("1.250", "1.300")
    issues = gate.safety_gate(BEFORE, after)
    assert issues and "cifras alteradas" in issues[0]
    assert "1.250" in issues[0] and "1.300" in issues[0]


def test_dropped_figure_rejected():
    after = BEFORE.replace(" en 3 fases", "")
    assert any("cifras alteradas" in i for i in gate.safety_gate(BEFORE, after))


def test_dropped_pendiente_rejected():
    after = BEFORE.replace("[PENDIENTE: fecha exacta]", "poco después.")
    assert any("PENDIENTE" in i for i in gate.safety_gate(BEFORE, after))


def test_added_emdash_rejected():
    after = BEFORE.replace("durante 2025.", "durante 2025 — un periodo intenso.")
    assert any("rayas em" in i for i in gate.safety_gate(BEFORE, after))


def test_inserted_editorial_marks_rejected():
    after = BEFORE.replace("línea base.", "línea base. [VERIFICAR: sin respaldo]")
    assert any("marcas editoriales" in i for i in gate.safety_gate(BEFORE, after))


def test_banned_term_rejected_only_with_list():
    after = BEFORE.replace("El sistema", "El sistema de AcmeSecreta")
    with_list = gate.safety_gate(BEFORE, after, ["AcmeSecreta"])
    without_list = gate.safety_gate(BEFORE, after, [])
    assert any("confidencialidad" in i for i in with_list)
    assert without_list == []


def test_preexisting_banned_term_not_flagged_as_new():
    before = BEFORE + "\nAcmeSecreta ya estaba aquí.\n"
    after = before.replace("Cada iteración", "Toda iteración")
    issues = gate.safety_gate(before, after, ["AcmeSecreta"])
    assert not any("confidencialidad" in i for i in issues)


def test_soft_check_warns_on_lost_emphasis():
    after = BEFORE.replace("todas las alternativas", "las alternativas")
    warns = gate.soft_checks(BEFORE, after)
    assert warns and "alcance" in warns[0]
    # soft, not blocking:
    assert gate.safety_gate(BEFORE, after) == []


def test_sentence_final_number_punctuation_not_a_figure_change():
    # '2 semanas.' -> rephrased so the number ends mid-sentence; token must stay '2'.
    after = BEFORE.replace("duró 2 semanas.", "duró 2 semanas, sin excepciones.")
    assert gate.safety_gate(BEFORE, after) == []
