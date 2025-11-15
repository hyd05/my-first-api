from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.payment import router as payment_router

app = FastAPI(title="LifeCoach AI Backend (FastAPI)")

app.include_router(chat_router)
app.include_router(payment_router)

@app.get('/')
def root():
    return {'message': 'LifeCoach AI Backend running'}

# Uygulamanızı burada tanımlayın (Örn: app = FastAPI())
app = FastAPI() 

# CORS ayarlarını tanımlıyoruz
origins = [
    "*", # **GEÇİCİ OLARAK** TÜM ADRESLERE İZİN VERİR. Güvenlik için daha sonra Figma URL'si ile değiştirilmelidir.
    "http://localhost:3000", # Eğer yerelde test ediyorsanız
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # Tüm HTTP metodlarına izin ver (GET, POST, PUT, DELETE, vb.)
    allow_headers=["*"],    # Tüm başlıklara izin ver
)

# ... buranın altına route'larınız (yollarınız) gelmeli
@app.get("/")
def read_root():
    return {"Hello": "World"}