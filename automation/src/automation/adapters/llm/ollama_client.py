"""Small local-only Ollama client for schema-constrained planning."""
from __future__ import annotations
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

class OllamaError(RuntimeError): pass


def _parse_json_object(response: str) -> dict[str, object] | None:
    """Recover a JSON object when a model adds fences or a short preamble."""
    candidates = [response.strip()]
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", response, re.DOTALL | re.IGNORECASE)
    if fenced:
        candidates.append(fenced.group(1))
    start, end = response.find("{"), response.rfind("}")
    if start >= 0 and end > start:
        candidates.append(response[start : end + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout_seconds: int = 180) -> None:
        self._url, self._model, self._timeout = f"{base_url}/api/generate", model, timeout_seconds
    def generate_json(self, prompt: str, schema: dict[str, object] | None = None) -> dict[str, object]:
        response_text = self._generate(prompt, schema)
        parsed = _parse_json_object(response_text)
        if parsed is not None:
            return parsed
        repair_prompt = (
            f"{prompt}\n\nYour previous answer was invalid. Return exactly one JSON object, with no markdown, explanation, or text before or after it."
        )
        response_text = self._generate(repair_prompt, schema)
        parsed = _parse_json_object(response_text)
        if parsed is not None:
            return parsed
        raise OllamaError("Gemma did not return a valid JSON object after two attempts. Try a shorter, more specific request.")

    def generate_text(self, prompt: str) -> str:
        """Generate a local chat reply; this method has no access to application tools."""
        return self._generate(prompt, None)

    def _generate(self, prompt: str, schema: dict[str, object] | None) -> str:
        payload = json.dumps({"model": self._model, "prompt": prompt, "format": schema or "json", "stream": False, "options": {"temperature": 0}}).encode()
        try:
            with urlopen(Request(self._url, payload, {"Content-Type": "application/json"}), timeout=self._timeout) as response:
                body = json.loads(response.read())
        except HTTPError as error:
            try:
                detail = json.loads(error.read().decode("utf-8")).get("error", "unknown server error")
            except (UnicodeDecodeError, json.JSONDecodeError):
                detail = "unknown server error"
            raise OllamaError(f"Ollama returned HTTP {error.code}: {detail}") from error
        except TimeoutError as error:
            raise OllamaError(f"Ollama did not finish within {self._timeout} seconds. Try a smaller document or request.") from error
        except URLError as error:
            raise OllamaError(f"Ollama cannot be reached at {self._url}: {error.reason}") from error
        except json.JSONDecodeError as error:
            raise OllamaError("Ollama returned invalid JSON before Gemma could respond.") from error
        if isinstance(body, dict) and body.get("error"):
            raise OllamaError(f"Ollama model error: {body['error']}")
        response_text = body.get("response") if isinstance(body, dict) else None
        if not isinstance(response_text, str):
            raise OllamaError("Ollama returned no model response")
        return response_text
