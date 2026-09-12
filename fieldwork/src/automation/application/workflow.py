"""The safe plan-preview-confirm-execute use case."""
from __future__ import annotations
from datetime import datetime, timezone
from collections.abc import Callable
from uuid import uuid4
from automation.application.confirmation import confirm
from automation.adapters.tools.spreadsheet_output import create_xlsx
from automation.domain.models import ExecutionResult, PlanStatus, UserRequest
from automation.application.invoice_planning import is_batch_invoice_request
from automation.application.certificate_planning import is_certificate_request
from automation.adapters.tools.certificate_output import certificate_filename, make_zip, render_certificate

class AutomationWorkflow:
    def __init__(self, artifacts: object, planner: object, plans: object, invoice_planner: object | None = None, certificate_planner: object | None = None) -> None:
        self._artifacts, self._planner, self._plans, self._invoice_planner, self._certificate_planner = artifacts, planner, plans, invoice_planner, certificate_planner

    def cleanup_expired(self, max_age_seconds: int) -> int:
        return self._artifacts.cleanup_expired(max_age_seconds)

    def output_path_for(self, artifact_id: str):
        return self._artifacts.output_path_for(artifact_id)
    def propose(self, instruction: str, input_paths: list[str], progress: Callable[[str], None] | None = None):
        emit = progress or (lambda _: None)
        emit("Validating uploaded files")
        artifacts = tuple(self._artifacts.ingest(__import__('pathlib').Path(path)) for path in input_paths)
        request = UserRequest(uuid4().hex, instruction, artifacts, datetime.now(timezone.utc))
        if self._certificate_planner is not None and is_certificate_request(instruction):
            emit("Checking certificate placeholders and Excel columns")
            plan, preview = self._certificate_planner.plan(request, artifacts, self._artifacts)
        else:
            emit(f"Reading {len(artifacts)} document(s)")
            documents = tuple((artifact, self._artifacts.read_text(artifact.artifact_id)) for artifact in artifacts)
            if self._invoice_planner is not None and is_batch_invoice_request(instruction):
                emit("Using the dedicated batch-invoice extractor")
                plan, preview = self._invoice_planner.plan(request, documents)
            else:
                emit("Asking Gemma to prepare a safe automation plan")
                text = "\n\n".join(source_text for _, source_text in documents)
                plan, preview = self._planner.plan(request, text)
        self._plans.save(plan, preview)
        emit("Preview is ready for your review")
        return plan, preview
    def execute(self, plan_id: str, approved: bool) -> ExecutionResult:
        plan, _ = self._plans.get(plan_id); confirmation = confirm(plan, approved, uuid4().hex)
        if not approved: return ExecutionResult(uuid4().hex, plan_id, PlanStatus.FAILED, datetime.now(timezone.utc), summary="Plan cancelled by user")
        plan = self._plans.claim(confirmation); action = plan.actions[0]; args = action.arguments
        if args["format"] == "certificate_batch":
            template = self._artifacts.path_for(str(args["template_artifact_id"]))
            files = {}
            for index, row in enumerate(args["rows"], start=1):
                content = render_certificate(template, dict(args["mapping"]), dict(row))
                files[certificate_filename(dict(row), index)] = content
            archive = self._artifacts.create_output("certificates.zip", "application/zip", make_zip(files))
            return ExecutionResult(uuid4().hex, plan_id, PlanStatus.COMPLETED, datetime.now(timezone.utc), (archive,), f"Created ZIP file containing {len(files)} certificate PDF(s)")
        if args["format"] == "xlsx":
            content = create_xlsx(args["columns"], args["rows"])
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            content = str(args["content"]).encode()
            media_type = "text/plain"
        output = self._artifacts.create_output(str(args["filename"]), media_type, content)
        return ExecutionResult(uuid4().hex, plan_id, PlanStatus.COMPLETED, datetime.now(timezone.utc), (output,), "Output created")
