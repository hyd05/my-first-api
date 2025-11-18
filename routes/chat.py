from fastapi import APIRouter, Depends
from models.request_models import ChatRequest
from services.gemini_service import ask_gemini
from services.security import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/message")
async def chat_message(req: ChatRequest, user=Depends(get_current_user)):
    # basic chat mode (free)
    prompt = "You are LifeCoach AI. Give a concise helpful answer.\nUser: " + req.prompt
    response = await ask_gemini(prompt, max_tokens=400)
    return {"response": response}
