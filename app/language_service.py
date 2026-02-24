import os
import requests

OPENCLAW_API_KEY = os.environ.get("OPENCLAW_API_KEY")

def translate_text(text, target_language):

    prompt = f"""
Translate the following text into {target_language}.
Keep formatting and bullet structure unchanged.

{text}
"""

    response = requests.post(
        "https://api.openclaw.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENCLAW_API_KEY}"
        },
        json={
            "model": "openclaw-model",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    return response.json()["choices"][0]["message"]["content"]