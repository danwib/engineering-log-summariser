from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE

_client = OpenAI(api_key=OPENAI_API_KEY)

def complete(system_prompt: str, user_prompt: str) -> str:
    resp = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return resp.choices[0].message.content.strip()
