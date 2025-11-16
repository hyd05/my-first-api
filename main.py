from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import secrets

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "LifeCoach AI Backend"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend is running"}

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    countryCode: str
    language: str

users_db = {}

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
    
    return {
        "success": True,
        "token": token,
        "user": {
            "name": request.name,
            "email": request.email,
            "language": request.language
        }
    }

class LoginRequest(BaseModel):
    email: str
    password: str

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

@app.get("/data")
async def get_data():
    return {
        "data": {
            "messages": [],
            "insights": [],
            "actionItems": [],
            "goals": [],
            "habits": []
        }
    }

@app.post("/save-data")
async def save_data():
    return {"success": True}

@app.get("/check-limit")
async def check_limit():
    return {
        "isPremium": False,
        "isTrialActive": True,
        "messageCount": 0,
        "limit": 10,
        "minutesUntilReset": 300
    }

@app.post("/increment-message")
async def increment_message():
    return {"messageCount": 1}
