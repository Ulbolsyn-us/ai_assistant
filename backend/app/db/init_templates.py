from app.api.models import Template
from app.db.session import SessionLocal

default_templates = {
    "needs_operator": "❗️Сейчас я передам ваш вопрос оператору. Ожидайте, пожалуйста.",
    "not_relevant": "❗️Извините, я могу отвечать только на вопросы по работе, собеседованиям и вакансиям.",
    "interview_invite": "📅 Ваше собеседование назначено на {date}, {time} (Zoom)\nСсылка: {link}\n\nПожалуйста, подтвердите участие 👇",
    "interview_confirm": "✅ Спасибо, участие подтверждено!"
}

def init_templates():
    db = SessionLocal()
    for name, content in default_templates.items():
        existing = db.query(Template).filter_by(name=name).first()
        if not existing:
            template = Template(name=name, content=content)
            db.add(template)
    db.commit()
    db.close()