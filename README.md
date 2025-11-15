LifeCoach AI — Python Backend (FastAPI)
======================================

Bu paket FastAPI tabanlı, Gemini API (AI chat) ve Payoneer ödeme endpoint'leri içeren örnek backend'dir.
Amaç: Supabase frontend veya başka bir frontend ile birlikte çalışacak, deploy'a hazır bir yapı sunmak.

⚠️ ÖNEMLİ: Bu örnek kod üretim öncesi test ve güvenlik kontrolüne ihtiyaç duyar. API anahtarlarınızı .env olarak sağlamalısınız.

Dosya yapısı:
- main.py
- routes/chat.py
- routes/payment.py
- services/gemini_service.py
- services/payoneer_service.py
- requirements.txt
- .env.example
- README.md (bu dosya)

Nasıl kullanılır (local):
1. Python 3.10+ kurulu olsun.
2. Sanal ortam oluşturup paketleri yükleyin:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. .env dosyanızı oluşturun (örnek .env.example referans alın):
   cp .env.example .env
   # .env içine GEMINI_API_KEY ve PAYONEER_API_KEY ve PAYONEER_PROGRAM_ID ekleyin
4. Uygulamayı çalıştırın:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
5. API:
   POST /chat  -> { "message": "merhaba" }
   POST /payment -> { "email": "user@example.com", "amount": 9.99 }

Deploy önerileri:
- Render, Railway, Fly.io veya Google Cloud Run üzerinde çalıştırabilirsiniz.
- Ortam değişkenlerini (API anahtarları) kesinlikle sunucu tarafında ayarlayın; frontend'de saklamayın.
