import os
import requests

OPENCLAW_API_KEY = os.environ.get("OPENCLAW_API_KEY")

def answer_question(question, transcript_chunks):

    context = "\n\n".join([chunk["text"] for chunk in transcript_chunks[:3]])

    prompt = f"""
Answer ONLY using the transcript context below.
If the answer is not found, respond exactly:
"This topic is not covered in the video."

Transcript Context:
{context}

Question:
{question}
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