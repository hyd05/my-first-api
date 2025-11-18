from services.gemini_service import ask_gemini

SYSTEM_PROMPT = """
You are LifeCoach AI. Provide deep emotional, psychological and supportive conversation.
Answer empathetically, suggest next steps, ask reflective questions, and provide contextual coping strategies.
"""

async def deep_conversation(user_prompt: str) -> str:
    prompt = SYSTEM_PROMPT + "\nUser: " + user_prompt + "\nAssistant:"
    return await ask_gemini(prompt, max_tokens=800)
