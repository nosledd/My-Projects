from automation.application.planning import _normalise_xlsx_rows


def test_single_cell_rows_are_transposed_into_one_record() -> None:
    assert _normalise_xlsx_rows(
        ["Invoice Number", "Customer Name", "Invoice Date", "Total Amount"],
        [["INV-42"], ["Aarav"], ["2026-07-28"], ["94.60"]],
    ) == [["INV-42", "Aarav", "2026-07-28", "94.60"]]


def test_object_rows_follow_the_declared_column_order() -> None:
    assert _normalise_xlsx_rows(
        ["Invoice Number", "Total Amount"],
        [{"Total Amount": "94.60", "Invoice Number": "INV-42"}],
    ) == [["INV-42", "94.60"]]
