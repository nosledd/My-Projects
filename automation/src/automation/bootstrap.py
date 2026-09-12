"""Application composition root."""
from __future__ import annotations
from pathlib import Path
from automation.adapters.llm.ollama_client import OllamaClient
from automation.adapters.storage.local_artifacts import LocalArtifactStore
from automation.adapters.storage.local_plans import LocalPlanRepository
from automation.application.planning import DocumentPlanner
from automation.application.invoice_planning import InvoiceBatchPlanner
from automation.application.certificate_planning import CertificatePlanner
from automation.application.workflow import AutomationWorkflow
from automation.configuration.settings import Settings
from automation.domain.policies import SafetyPolicy

def build(root: Path) -> AutomationWorkflow:
    settings = Settings.from_environment(root)
    artifacts = LocalArtifactStore(settings.uploads_dir, settings.outputs_dir)
    policy = SafetyPolicy()
    llm = OllamaClient(settings.ollama_url, settings.ollama_model)
    planner = DocumentPlanner(llm, policy)
    invoice_planner = InvoiceBatchPlanner(llm, policy)
    certificate_planner = CertificatePlanner(policy)
    return AutomationWorkflow(artifacts, planner, LocalPlanRepository(settings.plans_dir), invoice_planner, certificate_planner)
