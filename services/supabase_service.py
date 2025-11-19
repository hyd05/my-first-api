import os
from supabase import create_client
from supabase import Client
from dotenv import load_dotenv

load_dotenv()  # ENV Değişkenlerini yükle

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Önce güvenlik ve hata kontrolü
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Supabase bağlantı bilgileri eksik! Lütfen .env dosyanı kontrol et.")
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL.strip(), SUPABASE_KEY.strip())
    print("✔ Supabase bağlantısı başarılı")

def insert_journal(user_id: str, content: str):
    if not supabase:
        raise Exception("Supabase bağlantısı yapılamadı.")
    return supabase.table("journals").insert({"user_id": user_id, "content": content}).execute()

def get_journals(user_id: str):
    if not supabase:
        raise Exception("Supabase bağlantısı yapılamadı.")
    return supabase.table("journals").select("*").eq("user_id", user_id).execute()

def count_journals_today(user_id: str):
    if not supabase:
        raise Exception("Supabase bağlantısı yapılamadı.")
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return supabase.table("journals").select("*", count="exact").eq("user_id", user_id).gte("created_at", today).execute().count