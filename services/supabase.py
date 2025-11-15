from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

def save_message(message: str, reply: str):
    supabase.table("chat_history").insert({"message": message, "reply": reply}).execute()
supabase.table()