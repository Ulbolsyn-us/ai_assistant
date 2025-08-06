from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.db.session import init_db
from app.services.telegram_bot import start_bot
from app.routers.template_router import router as template_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_templates import init_templates
from app.api.hr_inbox import router as hrinbox_router
from app.api.invites import router as interview_invite


if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())

init_db()
init_templates()


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