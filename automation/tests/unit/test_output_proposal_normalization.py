from automation.application.planning import _requested_format, _safe_filename


def test_excel_request_overrides_a_friendly_model_format_name() -> None:
    assert _requested_format("Create an Excel report", "Excel") == "xlsx"


def test_filename_gets_the_expected_extension() -> None:
    assert _safe_filename("questionnaire_results", ".xlsx") == "questionnaire_results.xlsx"
    assert _safe_filename("questionnaire_results.csv", ".xlsx") == "questionnaire_results.xlsx"
