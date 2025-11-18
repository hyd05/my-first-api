from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(..., max_length=2000)

class JournalEntry(BaseModel):
    text: str = Field(..., max_length=5000)
