from fastapi import APIRouter, Depends
from app.db.schemas import ChatRequest, ChatResponse
from app.services.gpt_utils import ask_gpt
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api.models import Message
from app.services.nlp_utils import is_relevant_to_business
from app.api.templates import get_template_by_name


router = APIRouter()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
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
    forward_to_hr = is_relevant_to_business(request.message)
    
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
    return db.query(Message.timestamp.desc()).all()

