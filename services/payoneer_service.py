import os, httpx

PAYONEER_BASE = 'https://api.payoneer.com'  # production endpoint; confirm with Payoneer docs

async def create_payout(email: str, amount: float, currency: str = 'USD', description: str = 'LifeCoach AI Premium'):
    key = os.getenv('PAYONEER_API_KEY')
    program_id = os.getenv('PAYONEER_PROGRAM_ID')
    if not key or not program_id:
        raise RuntimeError('PAYONEER_API_KEY or PAYONEER_PROGRAM_ID not set')

    url = f"{PAYONEER_BASE}/v4/programs/{program_id}/payouts"
    body = {
        "payee_id": email,
        "amount": amount,
        "currency": currency,
        "description": description
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, json=body, headers=headers)
        res.raise_for_status()
        return res.json()
