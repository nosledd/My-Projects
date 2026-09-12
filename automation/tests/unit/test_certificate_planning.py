from automation.application.certificate_planning import is_certificate_request, normalise_name


def test_placeholder_and_excel_header_normalise_to_the_same_key() -> None:
    assert normalise_name("Register No") == normalise_name("REGISTER_NO")
    assert normalise_name("Event Date") == normalise_name("event_date")


def test_certificate_route_is_explicit() -> None:
    assert is_certificate_request("Generate certificates from this PDF and Excel sheet")
    assert not is_certificate_request("Extract this invoice into Excel")
