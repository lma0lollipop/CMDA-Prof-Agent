"""
ollama_client.py

Final stable Ollama client for CMDAProfAgent.
Uses /api/chat (Windows-safe) and non-streaming calls
for guaranteed output.
"""

import requests

# IMPORTANT:
# Ollama is already running on your system.
# Do NOT start ollama serve again if port is busy.

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "deepseek-r1"   # Use EXACT name from `ollama list`


def query_ollama(system_prompt: str, user_prompt: str) -> str:
    """
    Query Ollama using the chat API and return the full response text.
    """

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
            timeout=600
        )
        response.raise_for_status()

        data = response.json()

        # Ollama chat response format
        return data["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Ollama API error: {e}"
