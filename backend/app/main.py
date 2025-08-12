
import os
from fastapi import FastAPI, Request
import httpx
from telegram import Update
from backend.app.api.chat import router as chat_router
from backend.app.db.session import init_db
from backend.app.services.telegram_bot import start_bot, application
from backend.app.routers.template_router import router as template_router
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db.init_templates import init_templates
from backend.app.api.hr_inbox import router as hrinbox_router
from backend.app.api.invites import router as interview_invite

app = FastAPI()

app.include_router(chat_router)
app.include_router(template_router)
app.include_router(hrinbox_router)
app.include_router(interview_invite)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend is running"}

@app.on_event("startup")
async def on_startup():
    init_db()
    init_templates()
    await start_bot()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"status": "ok"}


@app.get("/test_openrouter")
async def test_openrouter():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Test API"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, can you respond?"}
        ]
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=data)
        return {"status": r.status_code, "response": r.text}