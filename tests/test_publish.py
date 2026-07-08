"""The typesetter must be config-driven end to end: no defaults, no leftovers."""
import publish
import pytest

docx = pytest.importorskip("docx")

MD = "# Metodología\n\nHubo 4.820 registros [F1]. Frase corta. Y una frase final algo más larga.\n"

CFG = {
    "project": {
        "title": "Título de prueba",
        "author": "Autora de Prueba",
        "university": "Universidad de Ejemplo",
        "degree": "Máster de Ejemplo",
        "academic_year": "2026/2027",
        "tutors": [{"role": "Tutora", "name": "Nombre Ejemplo"}],
    },
    "typography": {"font": "Arial", "size_pt": 11, "line_spacing": 1.5,
                   "margins_cm": {"top": 3, "bottom": 3, "left": 2.5, "right": 2.5}},
    "ai_disclosure": {"include": True, "tool": "Herramienta X", "assisted_phases": "edición"},
}


def _build(tmp_path, cfg, md=MD):
    out = tmp_path / "out.docx"
    publish.build_docx(md, str(out), cfg)
    return docx.Document(str(out))


def _texts(d):
    return [p.text for p in d.paragraphs if p.text.strip()]


def test_cover_comes_only_from_config(tmp_path):
    paras = _texts(_build(tmp_path, CFG))
    assert paras[0] == "Universidad de Ejemplo"
    assert "Tutora: Nombre Ejemplo" in paras
    assert "Curso académico: 2026/2027" in paras


def test_missing_cover_values_render_pendiente(tmp_path):
    paras = _texts(_build(tmp_path, {"project": {}, "typography": {}}))
    assert paras[0] == "[PENDIENTE: universidad]"
    assert not any("Daniel" in p or "Páez" in p for p in paras)


def test_strip_fact_tags():
    assert "[F1]" not in publish.strip_fact_tags(MD)
    assert "4.820 registros." in publish.strip_fact_tags(MD).replace("registros .", "registros.")


def test_headings_follow_config_font(tmp_path):
    d = _build(tmp_path, CFG)
    h1 = d.styles["Heading 1"]
    assert h1.font.name == "Arial"
    assert h1.font.size.pt == 15  # base 11 + 4
    assert str(h1.font.color.rgb) == "000000"


def test_page_number_field_except_cover(tmp_path):
    d = _build(tmp_path, CFG)
    s = d.sections[0]
    assert s.different_first_page_header_footer is True
    assert "PAGE" in s.footer.paragraphs[0]._p.xml


def test_toc_present_by_default_and_removable(tmp_path):
    with_toc = _build(tmp_path, CFG)
    assert "TOC" in with_toc.element.xml
    cfg = {**CFG, "typography": {**CFG["typography"], "include_toc": False}}
    out2 = tmp_path / "no_toc.docx"
    publish.build_docx(MD, str(out2), cfg)
    assert "TOC \\o" not in docx.Document(str(out2)).element.xml
