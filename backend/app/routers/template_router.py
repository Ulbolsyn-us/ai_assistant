from fastapi import APIRouter, HTTPException, Depends
from app.api.chat import get_db
from app.api.models import Template
from sqlalchemy.orm import Session
from app.api.templates import update_template

router = APIRouter()

@router.get("/templates")
def get_templates(db: Session = Depends(get_db)):
    templates = db.query(Template).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "content": t.content
        }
        for t in templates
    ]

@router.get("/templates/{template_key}")
def get_template(template_key: str, db: Session = Depends(get_db)):
    template = db.query(Template).filter_by(name=template_key).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {
        "id": template.id,
        "name": template.name,
        "content": template.content
    }

@router.put("/templates/{template_id}")
def update_template(template_id: int, updated_template: dict, db: Session = Depends(get_db)):
    template = db.query(Template).filter_by(id=template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if "content" not in updated_template:
        raise HTTPException(status_code=400, detail="Missing 'content' field")
    
    template.content = updated_template["content"]
    db.commit()
    return {"message": "Template updated", "template": {
        "id": template.id,
        "name": template.name,
        "content": template.content
    }}