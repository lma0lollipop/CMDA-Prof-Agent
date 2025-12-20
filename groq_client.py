from groq import Groq
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODEL_NAME = "llama-3.1-70b-versatile"


def query_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
