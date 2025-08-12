from fastapi import APIRouter, Depends
from backend.app.api.models import Message
from sqlalchemy.orm import Session
from backend.app.db.session import get_db

router = APIRouter()

@router.get("/hr-inbox")
def get_hrinbox(
):
    db = next(get_db())
    messages = db.query(Message).filter(Message.forwarded_to_hr == True).order_by(Message.timestamp.desc()).all()
    return [
        {
            "id": message.id,
            "user_id": message.user_id,
            "user_message": message.user_message,
            "bot_reply": message.bot_reply,
            "timestamp": message.timestamp.isoformat()
        }
        for message in messages
    ]
    