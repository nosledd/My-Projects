from datetime import datetime, timezone

from automation.application.invoice_planning import INVOICE_COLUMNS, InvoiceBatchPlanner, is_batch_invoice_request
from automation.domain.models import ArtifactKind, ArtifactReference, UserRequest
from automation.domain.policies import SafetyPolicy


class FakeInvoiceLlm:
    def generate_json(self, prompt: str, schema: dict[str, object]) -> dict[str, object]:
        return {"invoice_number": "INV-42", "customer_name": "Aarav Sharma", "invoice_date": "2026-07-28", "total_amount": 94.60, "currency": "USD"}


def test_invoice_batch_keeps_one_row_per_source_invoice() -> None:
    artifact = ArtifactReference("a1", ArtifactKind.FILE, "application/pdf", "hash", "invoice.pdf")
    request = UserRequest("r1", "Extract invoices into Excel", (artifact,), datetime.now(timezone.utc))
    _, preview = InvoiceBatchPlanner(FakeInvoiceLlm(), SafetyPolicy()).plan(request, ((artifact, "Invoice Number INV-42"),))
    assert preview.data["columns"] == list(INVOICE_COLUMNS)
    assert preview.data["rows"][0][1] == "INV-42"


def test_invoice_route_requires_invoice_and_excel_terms() -> None:
    assert is_batch_invoice_request("Extract three invoices into an Excel file")
    assert not is_batch_invoice_request("Summarize this invoice")
