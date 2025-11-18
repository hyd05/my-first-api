from services.gemini_service import ask_gemini

SYSTEM_PROMPT = """
You are LifeCoach AI's Life Plan Generator.
Produce a detailed, structured multi-year life plan. Include:
- Short-term (0-1 year) goals
- Medium-term (1-3 years) goals
- Long-term (3-5+ years) goals
- Concrete steps, estimated timeline, resources, risks, and motivation tips.
Format with headings and bullet points.
"""

async def generate_life_plan(goal_description: str) -> str:
    prompt = SYSTEM_PROMPT + "\nUser goal: " + goal_description + "\nPlan:"
    return await ask_gemini(prompt, max_tokens=1000)
