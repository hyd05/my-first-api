import os, httpx, asyncio

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"

async def generate_text(message: str) -> str:
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        raise RuntimeError('GEMINI_API_KEY not set')

    headers = {"Content-Type": "application/json"}
    payload = {"instances": [{"input": message}]}

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(f"{GEMINI_URL}?key={key}", json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        # adapt to response structure
        reply = "No reply"
        try:
            reply = data.get('candidates', [])[0].get('content', {}).get('parts', [])[0].get('text') or reply
        except Exception:
            # fallback
            reply = data.get('output', [{}])[0].get('content', 'No reply')
        return reply
