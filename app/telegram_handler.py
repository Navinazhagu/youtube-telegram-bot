from telegram import Update
from telegram.ext import ContextTypes

from transcript_service import extract_video_id, fetch_transcript
from chunking import chunk_transcript
from summarizer import generate_summary
from qa_engine import answer_question
from language_service import translate_text
from cache import video_cache, user_sessions


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # YouTube link handling
    if "youtube.com" in text or "youtu.be" in text:

        video_id = extract_video_id(text)
        if not video_id:
            await update.message.reply_text("Invalid YouTube link.")
            return

        transcript = fetch_transcript(video_id)
        if not transcript:
            await update.message.reply_text("Transcript not available for this video.")
            return

        chunks = chunk_transcript(transcript)
        full_text = " ".join([entry["text"] for entry in transcript])

        summary = generate_summary(full_text)

        video_cache[video_id] = chunks
        user_sessions[user_id] = {
            "video_id": video_id,
            "language": "English"
        }

        await update.message.reply_text(summary)
        return

    # Language change
    if "Hindi" in text:
        if user_id in user_sessions:
            user_sessions[user_id]["language"] = "Hindi"
            await update.message.reply_text("Language switched to Hindi.")
        else:
            await update.message.reply_text("Send a YouTube link first.")
        return

    # Question answering
    if user_id not in user_sessions:
        await update.message.reply_text("Please send a YouTube link first.")
        return

    session = user_sessions[user_id]
    video_id = session["video_id"]
    chunks = video_cache.get(video_id)

    if not chunks:
        await update.message.reply_text("Session expired. Please resend the YouTube link.")
        return

    answer = answer_question(text, chunks)

    if session["language"] != "English":
        answer = translate_text(answer, session["language"])

    await update.message.reply_text(answer)