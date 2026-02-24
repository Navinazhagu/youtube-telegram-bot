def chunk_transcript(transcript, chunk_size=1000):
    chunks = []
    current_text = ""
    start_time = transcript[0]["start"]

    for entry in transcript:
        text = entry["text"]
        if len(current_text) + len(text) < chunk_size:
            current_text += " " + text
        else:
            chunks.append({
                "text": current_text,
                "start": start_time,
                "end": entry["start"]
            })
            current_text = text
            start_time = entry["start"]

    if current_text:
        chunks.append({
            "text": current_text,
            "start": start_time,
            "end": transcript[-1]["start"]
        })

    return chunks