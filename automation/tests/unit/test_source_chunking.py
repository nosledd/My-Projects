from automation.application.planning import _source_chunks


def test_layout_pages_are_sent_as_individual_bounded_chunks() -> None:
    source = "[OCR_LAYOUT: positions]\n[PAGE 1]\nx=1:a1\n[PAGE 2]\nx=1:a2\n"
    chunks = _source_chunks(source)
    assert len(chunks) == 2
    assert all(chunk.startswith("[OCR_LAYOUT: positions]") for chunk in chunks)
    assert "[PAGE 1]" in chunks[0]
    assert "[PAGE 2]" in chunks[1]
