# app/model.py
from sqlalchemy import Column, Integer, String, Text
from .database import Base  # Base를 database 모듈에서 가져옵니다.

# 모델 정의
class FraudType(Base):
    __tablename__ = "fraud_types"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True, index=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    content = Column(Text, nullable=False)

class ServicePrompt(Base):
    __tablename__ = "service_prompts"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False, default="다음 대화가 어떤 사기 유형인지 판단합니다.")
