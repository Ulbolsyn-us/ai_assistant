from fastapi import APIRouter, Depends
from backend.app.db.schemas import ChatRequest, ChatResponse
from backend.app.services.gpt_utils import ask_gpt
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.api.models import Message
from backend.app.services.nlp_utils import is_relevant_to_business
from backend.app.api.templates import get_template_by_name


router = APIRouter()
        
def should_escalate(reply: str) -> bool:
    reply = reply.lower()
    vague_markers = [
        "не могу", "не уверен", "неизвестно", "непредсказуемо",
        "возможно", "может быть", "я не знаю", "трудно сказать",
        "лучше уточнить", "свяжитесь", "обратитесь", "рекомендую обратиться"
    ]

    too_generic = any(kw in reply for kw in vague_markers)
    # too_long = len(reply) > 300  # условие по длине

    return too_generic 

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    
    reply = await ask_gpt(request.message)
    
    if not is_relevant_to_business(request.message):
        # print("⚠️ Нерелевантное сообщение, но всё равно обрабатываем", request.message)
        return ChatResponse(
            reply = get_template_by_name("not_relevant")
        )
    
    
    needs_operator = should_escalate(reply)
    forward_to_hr = needs_operator and is_relevant_to_business(request.message)
    
    # 🔁 Если нужно передать оператору — заменяем ответ
    if needs_operator == True:
        reply = get_template_by_name("needs_operator")
    # print("✅ Сохраняем в БД:", request.message, "→", reply)
    db_message = Message(
        user_id=request.user_id,
        user_message=request.message,
        bot_reply=reply,
        needs_operator=needs_operator,
        forwarded_to_hr=forward_to_hr
    )
    db.add(db_message)
    db.commit()
    
    return ChatResponse(reply=reply)

@router.get("/messages")
def get_all_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp.desc()).all()
    return [
        {
            "id": m.id,
            "user_id": m.user_id,
            "user_message": m.user_message,
            "bot_reply": m.bot_reply,
            "timestamp": m.timestamp.isoformat(),
            "needs_operator": m.needs_operator,
            "forwarded_to_hr": m.forwarded_to_hr
            
        }
        for m in messages
    ]
