from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    user_message = Column(String)
    bot_reply = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    needs_operator =  Column(Boolean, default=False)
    forwarded_to_hr = Column(Boolean, default=False)
    
class InterviewInvite(Base):
    __tablename__ = "interview_invites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    interview_time = Column(String)
    confirmed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)