from fastapi import APIRouter, Depends, HTTPException
from models.request_models import ChatRequest
from services.lifeplan_service import generate_life_plan
from services.security import get_current_user

router = APIRouter(prefix="/lifeplan", tags=["Life Plan"])

@router.post("/generate")
async def lifeplan(req: ChatRequest, user=Depends(get_current_user)):
    if user.get("plan") != "premium":
        raise HTTPException(status_code=403, detail="Premium required")
    resp = await generate_life_plan(req.prompt)
    return {"life_plan": resp}
