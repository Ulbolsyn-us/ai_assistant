import asyncio
from fastapi import FastAPI, Request
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
    asyncio.create_task(start_bot())

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"status": "ok"}




