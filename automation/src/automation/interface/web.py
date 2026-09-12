"""Local browser workspace for safe automations, chat, and developer traces."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from email.parser import BytesParser
from email.policy import default
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock, Thread
from time import time
from urllib.parse import parse_qs
from uuid import uuid4

from automation.adapters.llm.ollama_client import OllamaClient
from automation.bootstrap import build
from automation.configuration.settings import Settings



PAGE = (Path(__file__).with_name("fieldwork.html").read_text(encoding="utf-8"))
_LEGACY_PAGE = r'''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Automate Local</title>
    <style>
      :root {
        --ink: #172033;
        --muted: #6b778c;
        --line: #e4e8ef;
        --blue: #2763eb;
        --blue-soft: #eef4ff;
        --surface: #fff;
        --canvas: #f7f9fc;
        --shadow: 0 16px 42px rgba(27, 48, 89, 0.08);
      }
      * {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        background: var(--canvas);
        color: var(--ink);
        font:
          14px Inter,
          ui-sans-serif,
          system-ui,
          -apple-system,
          Segoe UI,
          sans-serif;
      }
      .shell {
        max-width: 1480px;
        margin: auto;
        padding: 26px;
      }
      .top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 22px;
      }
      .brand {
        display: flex;
        gap: 11px;
        align-items: center;
        font-size: 18px;
        font-weight: 750;
      }
      .mark {
        display: grid;
        place-items: center;
        width: 33px;
        height: 33px;
        border-radius: 10px;
        background: var(--blue);
        color: #fff;
        font-size: 19px;
      }
      .local {
        border: 1px solid #bde4c5;
        background: #f0fbf3;
        color: #187337;
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 12px;
      }
      .grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 360px;
        gap: 20px;
        align-items: start;
      }
      .card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 17px;
        box-shadow: var(--shadow);
      }
      .workspace {
        min-width: 0;
        padding: 25px;
      }
      .eyebrow {
        color: var(--blue);
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }
      h1 {
        font-size: 27px;
        line-height: 1.2;
        margin: 6px 0 8px;
      }
      h2 {
        font-size: 16px;
        margin: 0 0 6px;
      }
      p {
        color: var(--muted);
        line-height: 1.5;
        margin: 0;
      }
      .drop {
        display: flex;
        min-height: 138px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1.5px dashed #c7d3ea;
        border-radius: 14px;
        background: #fbfcff;
        margin: 22px 0 16px;
        padding: 25px;
        text-align: center;
        cursor: pointer;
        transition:
          background 0.2s,
          border-color 0.2s;
      }
      .drop:hover,
      .drop.drag {
        border-color: var(--blue);
        background: var(--blue-soft);
      }
      .drop input {
        display: none;
      }
      .drop strong {
        display: block;
        margin-bottom: 5px;
      }
      .files {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        min-height: 25px;
      }
      .file {
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        background: #f1f5fb;
        border: 1px solid #dce5f1;
        border-radius: 8px;
        padding: 6px 9px;
        font-size: 12px;
      }
      .label {
        font-size: 12px;
        font-weight: 700;
        color: #43526b;
        margin: 15px 0 7px;
        display: block;
      }
      textarea {
        resize: vertical;
        width: 100%;
        min-height: 110px;
        border: 1px solid #d9e1ed;
        border-radius: 11px;
        padding: 13px;
        font: inherit;
        line-height: 1.45;
        outline: none;
      }
      textarea:focus {
        border-color: var(--blue);
        box-shadow: 0 0 0 3px #2763eb18;
      }
      .toggles {
        display: flex;
        gap: 7px;
        flex-wrap: wrap;
      }
      .toggle {
        border: 1px solid #dce4ef;
        background: #fff;
        border-radius: 9px;
        padding: 8px 11px;
        color: #48566c;
        cursor: pointer;
        font: inherit;
      }
      .toggle.active {
        border-color: var(--blue);
        background: var(--blue-soft);
        color: #174bbd;
        font-weight: 700;
      }
      .actions {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 19px;
        gap: 10px;
      }
      .hint {
        font-size: 12px;
      }
      .primary,
      .secondary {
        border: 0;
        border-radius: 9px;
        padding: 11px 15px;
        font: inherit;
        font-weight: 700;
        cursor: pointer;
      }
      .primary {
        background: var(--blue);
        color: #fff;
      }
      .primary:disabled {
        opacity: 0.55;
        cursor: not-allowed;
      }
      .secondary {
        background: #eef2f7;
        color: #334155;
      }
      .status {
        margin-top: 20px;
        padding: 14px;
        border-radius: 11px;
        background: #f8fafc;
        border: 1px solid var(--line);
        display: none;
      }
      .status.show {
        display: block;
      }
      .preview {
        margin-top: 18px;
        display: none;
      }
      .preview.show {
        display: block;
      }
      .table-wrap {
        overflow: auto;
        border: 1px solid var(--line);
        border-radius: 10px;
        margin-top: 10px;
      }
      table {
        border-collapse: collapse;
        width: 100%;
        font-size: 12px;
      }
      th,
      td {
        padding: 9px 11px;
        border-bottom: 1px solid var(--line);
        text-align: left;
        white-space: nowrap;
      }
      th {
        background: #f7f9fc;
        color: #45546a;
      }
      .side {
        display: flex;
        flex-direction: column;
        gap: 20px;
      }
      .chat {
        padding: 18px;
        height: 470px;
        display: flex;
        flex-direction: column;
      }
      .chatlog {
        flex: 1;
        overflow: auto;
        padding: 6px 2px;
      }
      .bubble {
        max-width: 89%;
        padding: 10px 12px;
        border-radius: 11px;
        margin: 9px 0;
        line-height: 1.45;
      }
      .bot {
        background: #f1f5fb;
        color: #24344f;
      }
      .user {
        background: var(--blue);
        color: #fff;
        margin-left: auto;
      }
      .chatrow {
        display: flex;
        gap: 7px;
        border-top: 1px solid var(--line);
        padding-top: 12px;
      }
      .chatrow input {
        min-width: 0;
        flex: 1;
        border: 1px solid #d9e1ed;
        border-radius: 9px;
        padding: 9px;
        font: inherit;
      }
      .dev {
        padding: 18px;
      }
      .dev summary {
        cursor: pointer;
        font-weight: 750;
      }
      .timeline {
        margin: 12px 0 0;
        padding: 0;
        list-style: none;
      }
      .timeline li {
        border-left: 2px solid #d9e4f9;
        padding: 0 0 11px 12px;
        margin-left: 5px;
        font-size: 12px;
        color: #536176;
      }
      .timeline li:last-child {
        padding-bottom: 0;
      }
      .timeline b {
        color: #25334b;
        display: block;
        margin-bottom: 2px;
      }
      .error {
        color: #b42318;
        background: #fff4f3;
        border-color: #f8c6c2;
      }
      @media (max-width: 940px) {
        .grid {
          grid-template-columns: 1fr;
        }
        .chat {
          height: 320px;
        }
        .shell {
          padding: 16px;
        }
      }
      @media (max-width: 560px) {
        .top {
          align-items: flex-start;
          gap: 10px;
        }
        .local {
          white-space: nowrap;
        }
        .workspace {
          padding: 18px;
        }
        .actions {
          align-items: stretch;
          flex-direction: column;
        }
        .primary,
        .secondary {
          width: 100%;
        }
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <header class="top">
        <div class="brand"><span class="mark">✦</span>Automate</div>
        <span class="local">● Local Gemma + local files</span>
      </header>
      <div class="grid">
        <main class="card workspace">
          <div class="eyebrow">Automation workspace</div>
          <h1>Turn documents into useful work.</h1>
          <p>
            Upload one or more files, choose an output target, and approve the
            exact result before anything is created.
          </p>
          <label class="drop" id="drop"
            ><input id="files" type="file" multiple /><strong
              >Drop documents here, or click to browse</strong
            ><span
              >PDF, Excel, DOCX, CSV, text, and supported local formats</span
            ></label
          >
          <div class="files" id="fileList"></div>
          <label class="label" for="prompt"
            >What would you like to automate?</label
          ><textarea
            id="prompt"
            placeholder="Extract invoice details from all uploaded documents and create one report."
          ></textarea
          ><span class="label">Output target</span>
          <div class="toggles" id="toggles">
            <button class="toggle active" data-format="auto">✦ Auto</button
            ><button class="toggle" data-format="certificate">Certificate</button
            ><button class="toggle" data-format="xlsx">▦ Excel</button
            ><button class="toggle" data-format="csv">⌁ CSV</button
            ><button class="toggle" data-format="json">{} JSON</button
            ><button class="toggle" data-format="txt">≡ Text</button>
          </div>
          <div class="actions">
            <span class="hint"
              >Files remain local. Creation always needs approval.</span
            ><button class="primary" id="run">Create safe preview →</button>
          </div>
          <section class="status" id="status"></section>
          <section class="preview" id="preview">
            <h2 id="previewTitle">Review output</h2>
            <p id="previewText"></p>
            <div class="table-wrap" id="table"></div>
            <div class="actions">
              <button class="secondary" id="cancel">Cancel</button
              ><button class="primary" id="approve">
                Approve & create file
              </button>
            </div>
          </section>
        </main>
        <aside class="side">
          <section class="card chat">
            <div>
              <div class="eyebrow">Chat</div>
              <h2>Talk with Gemma</h2>
              <p>Conversation only - it cannot access files or run tools.</p>
            </div>
            <div class="chatlog" id="chatlog">
              <div class="bubble bot">
                Hi! Ask me about automation ideas, prompts, or how your local
                setup works.
              </div>
            </div>
            <div class="chatrow">
              <input
                id="chatInput"
                placeholder="Ask Gemma anything..."
              /><button class="primary" id="chatSend">Send</button>
            </div>
          </section>
                   <section class="card dev"><details><summary>Developer activity</summary><p style="margin-top:7px">A local trace of this request. It shows stages, never full document content.</p><ul class="timeline" id="timeline"></ul></details></section> 
        </aside>
      </div>
    </div>

    <script>
      let selected = [],
        output = "auto",
        jobId = null,
        poll = null,
        planId = null;
      const $ = (id) => document.getElementById(id);
      const esc = (s) =>
        String(s ?? "").replace(
          /[&<>'"]/g,
          (c) =>
            ({
              "&": "&amp;",
              "<": "&lt;",
              ">": "&gt;",
              "'": "&#39;",
              '"': "&quot;",
            })[c],
        );
      function renderFiles() {
        $("fileList").innerHTML =
          selected
            .map(
              (f) =>
                `<span class="file">${esc(f.name)} · ${Math.ceil(f.size / 1024)} KB</span>`,
            )
            .join("") || '<span class="hint">No files selected yet</span>';
      }
      function setFiles(files) {
        selected = [...files];
        renderFiles();
      }
      renderFiles();
      $("files").onchange = (e) => setFiles(e.target.files);
      ["dragenter", "dragover"].forEach((n) =>
        $("drop").addEventListener(n, (e) => {
          e.preventDefault();
          $("drop").classList.add("drag");
        }),
      );
      ["dragleave", "drop"].forEach((n) =>
        $("drop").addEventListener(n, (e) => {
          e.preventDefault();
          $("drop").classList.remove("drag");
        }),
      );
      $("drop").addEventListener("drop", (e) => setFiles(e.dataTransfer.files));
      document.querySelectorAll(".toggle").forEach(
        (b) =>
          (b.onclick = () => {
            document
              .querySelectorAll(".toggle")
              .forEach((x) => x.classList.remove("active"));
            b.classList.add("active");
            output = b.dataset.format;
            if (output === "certificate") {
              $("prompt").value = "Generate certificates from the uploaded PDF template and Excel data.";
              $("prompt").placeholder = "Upload one certificate PDF and one XLSX student-data file.";
            }
          }),
      );
      function state(message, error = false) {
        const s = $("status");
        s.className = "status show" + (error ? " error" : "");
        s.textContent = message;
      }
      function events(items) {
        $("timeline").innerHTML = items
          .map(
            (x) =>
              `<li><b>${esc(x.message)}</b>${new Date(x.at * 1000).toLocaleTimeString()}</li>`,
          )
          .join("");
      }
      function preview(data) {
        planId = data.plan_id;
        $("preview").classList.add("show");
        $("previewTitle").textContent = data.summary;
        $("previewText").textContent =
          data.warnings?.join(" ") || "Nothing has been created yet.";
        const sample = data.data?.sample || data.data || {};
        const cols = sample.columns || [];
        const rows = sample.rows || [];
        $("table").innerHTML = cols.length
          ? `<table><thead><tr>${cols.map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((v) => `<td>${esc(v)}</td>`).join("")}</tr>`).join("")}</tbody></table>`
          : `<pre>${esc(JSON.stringify(sample, null, 2))}</pre>`;
      }
      async function check() {
        const r = await fetch("/api/jobs/" + jobId),
          j = await r.json();
        events(j.events || []);
        if (j.state === "failed") {
          clearInterval(poll);
          state(j.error, true);
          $("run").disabled = false;
        }
        if (j.state === "ready") {
          clearInterval(poll);
          state(
            "Preview ready. Review the result and approve only if it is correct.",
          );
          preview(j.preview);
          $("run").disabled = false;
        }
      }
      $("run").onclick = async () => {
        if (!selected.length || !$("prompt").value.trim())
          return state("Add at least one file and an instruction.", true);
        if (output === "certificate" && selected.length !== 2)
          return state("Certificate generation needs exactly one PDF template and one XLSX data file.", true);
        $("preview").classList.remove("show");
        $("run").disabled = true;
        state("Starting local automation…");
        const fd = new FormData();
        fd.append("instruction", $("prompt").value);
        fd.append("output_format", output);
        selected.forEach((f) => fd.append("files", f));
        const r = await fetch("/api/automation/start", {
            method: "POST",
            body: fd,
          }),
          j = await r.json();
        if (!r.ok) {
          state(j.error || "Could not start request.", true);
          $("run").disabled = false;
          return;
        }
        jobId = j.job_id;
        events([]);
        poll = setInterval(check, 900);
        check();
      };
      $("approve").onclick = async () => {
        const r = await fetch("/api/automation/confirm", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ plan_id: planId, approved: true }),
          }),
          j = await r.json();
        state(
          r.ok ? `${j.summary} Saved: ${j.outputs.join(", ")}` : j.error,
          !r.ok,
        );
        if (r.ok) $("preview").classList.remove("show");
      };
      $("cancel").onclick = () => {
        $("preview").classList.remove("show");
        state("Preview cancelled. No file was created.");
      };
      async function chat() {
        const input = $("chatInput"),
          message = input.value.trim();
        if (!message) return;
        input.value = "";
        $("chatlog").insertAdjacentHTML(
          "beforeend",
          `<div class="bubble user">${esc(message)}</div>`,
        );
        const r = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
          }),
          j = await r.json();
        $("chatlog").insertAdjacentHTML(
          "beforeend",
          `<div class="bubble bot">${esc(j.reply || j.error)}</div>`,
        );
        $("chatlog").scrollTop = 999999;
      }
      $("chatSend").onclick = chat;
      $("chatInput").onkeydown = (e) => {
        if (e.key === "Enter") chat();
      };
    </script>
  </body>
</html>
'''


@dataclass(slots=True)
class Job:
    job_id: str
    state: str = "running"
    events: list[dict[str, object]] = field(default_factory=list)
    preview: dict[str, object] | None = None
    error: str | None = None


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = Lock()

    def create(self) -> Job:
        job = Job(uuid4().hex)
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def event(self, job_id: str, message: str) -> None:
        with self._lock:
            self._jobs[job_id].events.append({"message": message, "at": time()})

    def finish(self, job_id: str, preview: dict[str, object]) -> None:
        with self._lock:
            job = self._jobs[job_id]; job.preview = preview; job.state = "ready"

    def fail(self, job_id: str, error: str) -> None:
        with self._lock:
            job = self._jobs[job_id]; job.error = error; job.state = "failed"

    def get(self, job_id: str) -> dict[str, object] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            # Do not use dataclasses.asdict here: preview data may contain the
            # immutable MappingProxyType used by the domain layer, which cannot
            # be deep-copied. Convert it directly into JSON-safe values instead.
            return _json_value({
                "job_id": job.job_id,
                "state": job.state,
                "events": job.events,
                "preview": job.preview,
                "error": job.error,
            })


def _json_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_json_value(item) for item in value]
    return value


class AutomationHandler(BaseHTTPRequestHandler):
    workflow = None
    chat_client: OllamaClient
    root: Path
    jobs = JobStore()

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            self._html(PAGE)
        elif self.path.startswith("/api/jobs/"):
            job = self.jobs.get(self.path.rsplit("/", 1)[-1])
            self._json(job or {"error": "Job not found"}, HTTPStatus.OK if job else HTTPStatus.NOT_FOUND)
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        try:
            if self.path == "/api/automation/start": self._start_automation()
            elif self.path == "/api/automation/confirm": self._confirm()
            elif self.path == "/api/chat": self._chat()
            else: self._json({"error": "Route not found"}, HTTPStatus.NOT_FOUND)
        except Exception as error:
            self._json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

    def _start_automation(self) -> None:
        fields = self._form()
        instruction = self._field(fields, "instruction")
        output_format = self._field(fields, "output_format")
        if output_format and output_format != "auto": instruction += f"\n\nRequested output format: {output_format.upper()}."
        paths = self._save_uploads(fields)
        if not instruction.strip() or not paths: raise ValueError("Provide an instruction and at least one file.")
        job = self.jobs.create(); self.jobs.event(job.job_id, "Upload received; preparing local workspace")
        Thread(target=self._run_job, args=(job.job_id, instruction, paths), daemon=True).start()
        self._json({"job_id": job.job_id}, HTTPStatus.ACCEPTED)

    def _run_job(self, job_id: str, instruction: str, paths: list[str]) -> None:
        try:
            plan, preview = self.workflow.propose(instruction, paths, lambda message: self.jobs.event(job_id, message))
            self.jobs.finish(job_id, {"plan_id": plan.plan_id, "summary": preview.summary, "data": _json_value(preview.data), "warnings": list(preview.warnings)})
        except Exception as error:
            self.jobs.fail(job_id, str(error))

    def _confirm(self) -> None:
        body = self._body_json(); plan_id = str(body.get("plan_id", "")); approved = bool(body.get("approved"))
        result = self.workflow.execute(plan_id, approved)
        self._json({"summary": result.summary, "outputs": [artifact.display_name for artifact in result.output_artifacts]})

    def _chat(self) -> None:
        message = str(self._body_json().get("message", "")).strip()
        if not message: raise ValueError("Chat message is required.")
        prompt = "You are Gemma in a local AI automation workspace. Answer helpfully and concisely. You cannot access uploaded files, execute tools, or create files from chat.\n\nUser: " + message
        self._json({"reply": self.chat_client.generate_text(prompt)})

    def _form(self) -> dict[str, list[tuple[str, bytes]]]:
        content_type = self.headers.get("Content-Type", ""); length = int(self.headers.get("Content-Length", "0"))
        if length > 25 * 1024 * 1024: raise ValueError("Uploads are limited to 25 MB per request.")
        body = self.rfile.read(length)
        if content_type.startswith("application/x-www-form-urlencoded"):
            return {name: [("", value.encode()) for value in values] for name, values in parse_qs(body.decode("utf-8", "replace"), keep_blank_values=True).items()}
        message = BytesParser(policy=default).parsebytes(f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode() + body)
        fields: dict[str, list[tuple[str, bytes]]] = {}
        for part in message.iter_parts():
            fields.setdefault(part.get_param("name", header="content-disposition") or "", []).append((part.get_filename() or "", part.get_payload(decode=True) or b""))
        return fields

    def _save_uploads(self, fields: dict[str, list[tuple[str, bytes]]]) -> list[str]:
        directory = self.root / "data" / "workspace" / "web_uploads"; directory.mkdir(parents=True, exist_ok=True)
        paths: list[str] = []
        for filename, content in fields.get("files", []):
            name = Path(filename).name
            if name:
                target = directory / f"{uuid4().hex}_{name}"; target.write_bytes(content); paths.append(str(target))
        return paths

    @staticmethod
    def _field(fields: dict[str, list[tuple[str, bytes]]], name: str) -> str:
        return fields.get(name, [("", b"")])[0][1].decode("utf-8", "replace")

    def _body_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0")); body = json.loads(self.rfile.read(length))
        if not isinstance(body, dict): raise ValueError("JSON object expected.")
        return body

    def _json(self, body: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(body).encode(); self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def _html(self, content: str) -> None:
        data = content.encode(); self.send_response(HTTPStatus.OK); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None: return


def serve(root: Path, host: str = "127.0.0.1", port: int = 8080) -> None:
    AutomationHandler.root = root.resolve(); AutomationHandler.workflow = build(AutomationHandler.root)
    settings = Settings.from_environment(AutomationHandler.root)
    AutomationHandler.chat_client = OllamaClient(settings.ollama_url, settings.ollama_model)
    server = ThreadingHTTPServer((host, port), AutomationHandler)
    print(f"Open http://{host}:{port} in your browser. Press Ctrl+C to stop.")
    server.serve_forever()
