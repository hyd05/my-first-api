import os
from supabase import create_client, Client
from datetime import date

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# helper functions
def insert_journal(user_id: str, text: str, reflection: str):
    today = date.today().isoformat()
    res = supabase.table("journal").insert({
        "user_id": user_id,
        "entry": text,
        "reflection": reflection,
        "date": today
    }).execute()
    return res

def get_journals(user_id: str):
    res = supabase.table("journal").select("*").eq("user_id", user_id).order("date", desc=True).execute()
    return res.data if hasattr(res, "data") else []
    
def count_journals_today(user_id: str) -> int:
    today = date.today().isoformat()
    res = supabase.table("journal").select("id").eq("user_id", user_id).eq("date", today).execute()
    if hasattr(res, "data"):
        return len(res.data)
    return 0
