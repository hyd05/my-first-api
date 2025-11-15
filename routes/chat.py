from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import generate_text

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat_endpoint(req: ChatRequest):
    try:
        reply = await generate_text(req.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
