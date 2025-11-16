from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import secrets
import os
import httpx  # Gemini API için

app = FastAPI()

app.config[""] = ""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CORS = app.get_app()
users_db = {}
user_data_db = {}



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

#AUTH ENDPOINTS 

@app.get("/")
async def root():
    return {"status": "ok", "message": "LifeCoach AI Backend"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend is running"}

@app.post("/signup")
async def signup(request: SignupRequest):
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
    
    # Initialize user data
    user_data_db[token] = {
        "messages": [],
        "insights": [],
        "actionItems": [],
        "goals": [],
        "habits": []
    }
    
    return {
        "success": True,
        "token": token,
        "user": {
            "name": request.name,
            "email": request.email,
            "language": request.language,
            "countryCode": request.countryCode
        }
    }

@app.post("/login")
async def login(request: LoginRequest):
    if request.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[request.email]
    if user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "success": True,
        "token": user["token"],
        "user": {
            "name": user["name"],
            "email": request.email,
            "language": user["language"]
        }
    }

#GEMİNİ END POİNT

@app.post("/chat")
async def chat(request: ChatRequest, authorization: str = Header(None)):
    # Token kontrolü
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    if token not in user_data_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Gemini API Key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    # System prompt - dile göre
    system_prompts = {
        "tr": "Sen empatik ve destekleyici bir kişisel gelişim koçusun. Kullanıcıya motivasyon ver, hedeflerine ulaşmasına yardımcı ol ve yapıcı geri bildirimler sun. Kısa ve net cevaplar ver.",
        "en": "You are an empathetic and supportive personal development coach. Motivate the user, help them achieve their goals, and provide constructive feedback. Keep responses concise and clear.",
        "de": "Du bist ein einfühlsamer und unterstützender persönlicher Entwicklungscoach. Motiviere den Benutzer, hilf ihm, seine Ziele zu erreichen, und gib konstruktives Feedback. Halte die Antworten kurz und klar."
    }
    
    system_prompt = system_prompts.get(request.language, system_prompts["en"])
    
    # Gemini API çağrısı
    try:
        async with httpx.AsyncClient() as client:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
            
            gemini_request = {
                "contents": [{
                    "parts": [{
                        "text": f"{system_prompt}\n\nKullanıcı: {request.message}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 500
                }
            }
            
            response = await client.post(gemini_url, json=gemini_request, timeout=30.0)
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Gemini API error: {response.text}")
            
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            
            return {
                "success": True,
                "response": ai_response
            }
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Gemini API timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

# DATA ENDPOİNT

@app.get("/data")
async def get_data(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    
    if token in user_data_db:
        return {"data": user_data_db[token]}
    else:
        # Initialize empty data
        user_data_db[token] = {
            "messages": [],
            "insights": [],
            "actionItems": [],
            "goals": [],
            "habits": []
        }
        return {"data": user_data_db[token]}

@app.post("/save-data")
async def save_data(request: SaveDataRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    user_data_db[token] = request.data
    
    return {"success": True}

@app.get("/check-limit")
async def check_limit(authorization: str = Header(None)):
    return {
        "isPremium": False,
        "isTrialActive": True,
        "messageCount": 0,
        "limit": 10,
        "minutesUntilReset": 300
    }

@app.post("/increment-message")
async def increment_message(authorization: str = Header(None)):
    return {"messageCount": 1}