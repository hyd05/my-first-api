from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import secrets
from pathlib import Path
from typing import Any, Dict, Optional, List, Union


# Load envirofrom fastapi import FastAPI, HTTPException, Header

load_dotenv()

# ========== Rate Limiting ==========
limiter = Limiter(key_func=get_remote_address)

# ========== FastAPI Initialization ==========
app = FastAPI(
    title="LifeCoach AI Backend",
    description="Backend system for LifeCoach AI by HAN AI Technology",
    version="1.0.1"
)

# Apply rate limiting
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ========== CORS Configuration ==========
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not origins or origins == [""]:
    origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["*"],  # '*' sadece test aşamasında
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Temporary In-Memory Databases ==========
users_db = {}       # Kullanıcı bilgileri
user_data_db = {}   # Kullanıcı mesajları / içgörüleri


# ========== Pydantic Models ==========
class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    countryCode: str
    language: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SaveDataRequest(BaseModel):
    data: dict


# ========== Core System Endpoints ==========

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "LifeCoach AI Backend is ready.",
        "version": "1.0.1",
        "company": "HAN AI Technology"
    }

@app.post("/signup")
async def signup(request: SignupRequest):
    if request.email in users_db:
        raise HTTPException(status_code=409, detail="Email already registered")

    token = secrets.token_urlsafe(32)
    users_db[request.email] = {
        "password": request.password,  # Production'da hash yapılmalı
        "name": request.name,
        "countryCode": request.countryCode,
        "language": request.language,
        "token": token
    }
    user_data_db[token] = {"messages": [], "insights": []}
    return {"success": True, "token": token}

@app.post("/login")
async def login(request: LoginRequest):
    user = users_db.get(request.email)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "token": user["token"]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ========== Include External Modules ==========
from routes import chat as chat_router, deep_conversation, lifeplan, journal, payment

# Production standard: prefix ile daha düzenli
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat Module"])
app.include_router(deep_conversation.router, prefix="/api/deep", tags=["Deep Mode"])
app.include_router(lifeplan.router, prefix="/api/lifeplan", tags=["Life Plan"])
app.include_router(journal.router, prefix="/api/journal", tags=["Journal"])
app.include_router(payment.router, prefix="/api/payment", tags=["Payment"])

# determine main.py location and look for .env there
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"

# Print debug info to help troubleshooting
print(f"[DEBUG] Python cwd: {Path.cwd()}")
print(f"[DEBUG] main.py path: {Path(__file__).resolve()}")
print(f"[DEBUG] Looking for .env at: {dotenv_path}")

# Try load .env from that exact path
if dotenv_path.exists():
    load_dotenv(dotenv_path)
    print("[DEBUG] .env loaded from project directory")
else:
    # fallback: try load default (current working dir)
    load_dotenv()
    print("[DEBUG] .env NOT found in project dir, attempted default load()")

# quick print (don't reveal secret in logs in production)
print("[DEBUG] SUPABASE_URL set?:", bool(os.getenv("SUPABASE_URL")))
print("[DEBUG] SUPABASE_KEY set?:", bool(os.getenv("SUPABASE_KEY")))
# ---------------------------------------------------------------------