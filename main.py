from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.payment import router as payment_router

app = FastAPI(title="LifeCoach AI Backend (FastAPI)")

app.include_router(chat_router)
app.include_router(payment_router)

@app.get('/')
def root():
    return {'message': 'LifeCoach AI Backend running'}
