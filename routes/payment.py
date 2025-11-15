from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.payoneer_service import create_payout

router = APIRouter(prefix="/payment", tags=["payment"])

class PaymentRequest(BaseModel):
    email: str
    amount: float
    currency: str = "USD"
    description: str = "LifeCoach AI Premium"

@router.post("/")
async def payment_endpoint(req: PaymentRequest):
    try:
        data = await create_payout(req.email, req.amount, req.currency, req.description)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
