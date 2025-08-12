from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.api.models import Template


def get_template_by_name(name: str) -> str:
    template = db.query(Template).filter_by(name=name).first()
    return template.content if template else ""

def update_template(name: str, new_content: str, db: Session = Depends(get_db)) -> bool:
    template = db.query(Template).filter_by(name=name).first()
    db = next(get_db())
    if template:
        template.content = new_content
    else:
        template = Template(name=name, content=new_content)
        db.add(template)
    db.commit()
    return True