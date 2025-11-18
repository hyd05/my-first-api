from fastapi import APIRouter, Depends, HTTPException
from models.request_models import ChatRequest
from services.conversation_service import deep_conversation
from services.security import get_current_user

router = APIRouter(prefix="/deep", tags=["Deep Conversation"])

@router.post("/conversation")
async def deep_conv(req: ChatRequest, user=Depends(get_current_user)):
    if user.get("plan") != "premium":
        raise HTTPException(status_code=403, detail="Premium required")
    resp = await deep_conversation(req.prompt)
    return {"response": resp}
