import os
import requests
import base64

class OllamaError(RuntimeError):
    pass

def generate_description(prompt: str, image_bytes: bytes, model: str | None = None, url: str | None = None, timeout: int = 30) -> str:
    """Send prompt and image to Ollama-compatible HTTP endpoint and return text.

    This function assumes Ollama is the primary/only backend. If the server is
    unreachable or returns an error, an exception is raised.
    """
    url = url or os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model = model or os.getenv("OLLAMA_MODEL", "gpt-4o-mini")

    image_b64 = base64.b64encode(image_bytes).decode()
    payload = {
        "model": model,
        "prompt": prompt,
        "image": image_b64,
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except Exception as e:
        raise OllamaError(f"Failed to contact Ollama at {url}: {e}") from e

    try:
        resp.raise_for_status()
    except Exception as e:
        raise OllamaError(f"Ollama returned error status: {resp.status_code} {resp.text}") from e

    try:
        data = resp.json()
        return data.get("text") or data.get("output") or data.get("result") or resp.text
    except ValueError:
        return resp.text
