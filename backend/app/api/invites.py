from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import StreamingResponse
import csv
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.api.models import InterviewInvite
from app.db.session import get_db
from io import StringIO





router = APIRouter()

@router.get("/invites")
def get_invites(
    db: Session = Depends(get_db),
    user_id: Optional[str] = Query(None),
    date: Optional[str] = Query(None)
):
    query = db.query(InterviewInvite)
    
    if user_id: 
        query = query.filter(InterviewInvite.user_id == user_id)
        
    if date: 
        try: 
            day_start = datetime.strptime(date, "%Y-%m-%d")
            day_end = day_start + timedelta(days=1)
            
            query = query.filter(
                InterviewInvite.timestamp >= day_start,
                InterviewInvite.timestamp < day_end
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    results = query.order_by(InterviewInvite.timestamp.desc()).all()

    return [
        {
            "id": invite.id,
            "user_id": invite.user_id,
            "interview_time": invite.interview_time,
            "confirmed": invite.confirmed,
            "timestamp": invite.timestamp
        }
        for invite in results
    ]

@router.delete("/invites/{invite_id}")
def delete_invite(invite_id: int, db: Session = Depends(get_db)):
    invite = db.query(InterviewInvite).filter_by(id=invite_id).first()
    if not invite: 
        raise HTTPException(status_code=404, detail="Invite not found")
    db.delete(invite)
    db.commit()
    return {"message": "Invite deleted"}

@router.get("/invites/export/csv")
def export_invites_csv(db: Session = Depends(get_db)):
    invites = db.query(InterviewInvite).order_by(InterviewInvite.timestamp.desc()).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User ID", "Interview Time", "Confirmed", "Timestamp"])
    
    for invite in invites:
        writer.writerow([
            invite.id,
            invite.user_id,
            invite.interview_time,
            invite.confirmed,
            invite.timestamp
        ])
        
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=invites.csv"
    })
