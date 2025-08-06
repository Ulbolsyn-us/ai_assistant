from fastapi import Depends
from sqlalchemy.orm import Session
import os 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    ContextTypes, 
    MessageHandler, 
    CallbackQueryHandler, 
    filters) # обработчик сообщений (MessageHandler) / обработчик callback-кнопок (CallbackQueryHandler) — для ответа на нажатие.
from dotenv import load_dotenv
from app.api.models import Message, InterviewInvite
from app.db.session import get_db
import httpx
from app.api.templates import get_template_by_name


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# 🟡 Функция обработки входящих сообщений

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Session = Depends(get_db)):
    if update.message is None or update.message.text is None:
        return
    
    user_message = update.message.text
    user_id = str(update.message.from_user.id)
    
    # Игнорируем callback data как текст
    
    if user_message.strip().lower() == "confirm_interview":
        return
    
    if "собеседование" in user_message.lower():
        text = get_template_by_name("interview_invite").format(
            date="26 июня",
            time="15:00",
            link="https://zoom.us/test"
        )
        
        # Кнопка подтверждения
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Подтвердить участие", callback_data="confirm_interview")]
        ])
        
        # Отправляем приглашение
        
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )
        
        db_message = Message(
            user_id=user_id,
            user_message=user_message,
            bot_reply="📅 Приглашение на собеседование отправлено"
        )
        db.add(db_message)
        db.commit()
        
        return
    
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            "http://localhost:8000/chat",
            json={
                "message": user_message,
                "user_id": user_id
                }
        )
        data = response.json()
        bot_reply = data["reply"]
        
        await update.message.reply_text(bot_reply)
    
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Session = Depends(get_db)):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    print(f"Пользователь {user_id} подтвердил участие")
    
    # Сохраняем подтверждение в InterviewInvite
    invite = InterviewInvite(
        user_id=user_id,
        interview_time="2025-06-26 15:00",
        confirmed=True
    )
    db.add(invite)
    db.commit()
    
    # Здесь можно сохранить в БД таблицу подтверждений (если нужно)
    await query.edit_message_text("Спасибо, участие подтверждено!")
    
def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Обработка текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработка нажатий на inline-кнопки
    app.add_handler(CallbackQueryHandler(handle_button_click))
    
    print("Telegram бот запущен")
    app.run_polling()
    
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())
    
    
print("✅ Бот стартует...")