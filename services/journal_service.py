from services.gemini_service import ask_gemini
from services.supabase_service import insert_journal, get_journals, count_journals_today
from fastapi import HTTPException

async def save_journal_entry(user_id: str, text: str):
    # generate reflection
    reflection_prompt = f"Read the following journal entry and give a short empathetic reflection (2-4 sentences):\n\n{text}"
    reflection = await ask_gemini(reflection_prompt, max_tokens=200)
    # save to supabase
    insert_journal(user_id, text, reflection)
    return reflection

async def get_journal_entries(user_id: str):
    return get_journals(user_id)

def check_daily_limit(user_id: str):
    cnt = count_journals_today(user_id)
    if cnt >= 1:
        raise HTTPException(status_code=429, detail="Daily free journal limit reached")
