import os
import requests

OPENCLAW_API_KEY = os.environ.get("OPENCLAW_API_KEY")

def generate_summary(transcript_text):

    prompt = f"""
You are an AI research assistant.

Summarize the following YouTube transcript in structured format:

 Title
 5 Key Points
 Important Timestamps
 Core Takeaway

Transcript:
{transcript_text[:6000]}
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