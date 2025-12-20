import requests

OLLAMA_URL = "https://fireless-subcordately-coreen.ngrok-free.dev/api/chat"
MODEL_NAME = "deepseek-r1"


def query_ollama(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            },
            timeout=600
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Ollama API error: {e}"
