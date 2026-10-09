from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL_NAME = "qwen/qwen3.8-27b"
MAX_TOKENS = 2048   # SAFE VALUE


def query_llm(system_prompt: str, user_prompt: str) -> str:
    # Safety trimming (VERY IMPORTANT)
    system_prompt = system_prompt[:8000]
    user_prompt = user_prompt[:8000]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=MAX_TOKENS
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Groq API error: {e}"
