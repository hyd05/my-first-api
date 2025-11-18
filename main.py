from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
import os
from dotenv import load_dotenv
import secrets
import os
import httpx

# Uygulama Objesini Tanımlama
app = FastAPI()

# --- 1. CORS Middleware ---
# Bu ayar, tarayıcıların (Figma dahil) API'nize erişmesini sağlar.
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------


# In-memory storage (Bu veri, sunucu her yeniden başladığında SIFIRLANIR!)
users_db = {}
user_data_db = {}


# ============= MODELLER =============
class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    countryCode: str
    language: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    message: str
    language: str

class SaveDataRequest(BaseModel):
    data: dict


# ============= ROUTE'LAR (YOLLAR) =============

@app.get("/")
async def root():
    return {"status": "ok", "message": "LifeCoach AI Backend is operational"}

@app.post("/signup")
async def signup(request: SignupRequest):
    # ... (Signup loğiği) ...
    if request.email in users_db:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    token = secrets.token_urlsafe(32)
    users_db[request.email] = {
        "password": request.password,
        "name": request.name,
        "countryCode": request.countryCode,
        "language": request.language,
        "token": token
    }
    user_data_db[token] = {"messages": [], "insights": []} # Basit başlatma
    
    return {"success": True, "token": token}


@app.post("/login")
async def login(request: LoginRequest):
    # ... (Login loğiği) ...
    if request.email not in users_db or users_db[request.email]["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[request.email]
    return {"success": True, "token": user["token"]}


@app.post("/chat")
async def chat(request: ChatRequest, authorization: str = Header(None)):
    # ... (Chat ve Gemini loğiği) ...
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    if token not in user_data_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Gemini API Key Kontrolü
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    # Kalan Gemini loğiği (httpx ile API çağrısı)
    try:
        async with httpx.AsyncClient() as client:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
            
            # Request body'yi basitleştirdim
            gemini_request = {
                "contents": [{"parts": [{"text": request.message}]}]
            }
            
            response = await client.post(gemini_url, json=gemini_request)
            
            if response.status_code != 200:
                # API'den gelen hatayı göstermek için
                raise HTTPException(status_code=500, detail=f"Gemini API error: {response.text}")
            
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            
            return {"success": True, "response": ai_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend is running"}

load_dotenv()

app = FastAPI(title="LifeCoach AI Backend")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if origins == [""]:
    origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from routes import chat, deep_conversation, lifeplan, journal, payment

app.include_router(chat.router)
app.include_router(deep_conversation.router)
app.include_router(lifeplan.router)
app.include_router(journal.router)
app.include_router(payment.router)

@app.get("/health")
async def health():
    return {"status": "ok"}