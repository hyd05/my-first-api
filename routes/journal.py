from fastapi import APIRouter, Depends
from models.request_models import JournalEntry
from services.journal_service import save_journal_entry, get_journal_entries, check_daily_limit
from services.security import get_current_user

router = APIRouter(prefix="/journal", tags=["Journal"])

@router.post("/write")
async def write(entry: JournalEntry, user=Depends(get_current_user)):
    if user.get("plan", "free") == "free":
        # enforce limit
        check_daily_limit(user["id"])
    reflection = await save_journal_entry(user["id"], entry.text)
    return {"saved": True, "reflection": reflection}

@router.get("/history")
async def history(user=Depends(get_current_user)):
    return {"entries": await get_journal_entries(user["id"])}
