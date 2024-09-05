# controller.py
import os
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .model import FraudType, Conversation, ServicePrompt
import openai
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하기 위해 사용

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수에서 OpenAI API 키를 가져옵니다.
openai.api_key = os.getenv("OPENAI_API_KEY")  # 실제 사용 시 자신의 API 키를 .env 파일에 설정하세요.

router = APIRouter()

# 대화 분석 웹소켓 요청 처리
@router.websocket("/ws/analyze_conversation")
async def analyze_conversation(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        conversation = data.get("conversation")
        
        # 모든 사기 유형을 데이터베이스에서 가져옵니다.
        fraud_types = db.query(FraudType).all()
        fraud_type_list = [fraud.type for fraud in fraud_types]
        fraud_types_text = ", ".join(fraud_type_list)  # 사기 유형을 문자열로 변환
        
        # 현재 서비스 프롬프트 가져오기
        prompt = db.query(ServicePrompt).first()
        prompt_text = prompt.prompt if prompt else "다음 대화가 어떤 사기 유형인지 판단합니다."

        # 모든 사기 유형과 대화 내용을 GPT 모델에 전달
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"현재 알려진 사기 유형: {fraud_types_text}. {prompt_text}"},
                {"role": "user", "content": conversation}
            ]
        )
        result = response['choices'][0]['message']['content']
        await websocket.send_text(result)
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

# 기존의 사기 유형 추가, 삭제, 프롬프트 관리 엔드포인트 등 다른 기능은 유지됩니다.
# 사기 유형 추가
@router.websocket("/ws/add_fraud_type")
async def add_fraud_type(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        fraud_type = FraudType(type=data.get("type"))
        db.add(fraud_type)
        db.commit()
        await websocket.send_text(f"Fraud type '{fraud_type.type}' added successfully")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

# 사기 유형 삭제
@router.websocket("/ws/delete_fraud_type")
async def delete_fraud_type(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        fraud_type = data.get("type")
        fraud = db.query(FraudType).filter(FraudType.type == fraud_type).first()
        if fraud:
            db.delete(fraud)
            db.commit()
            await websocket.send_text(f"Fraud type '{fraud_type}' deleted successfully")
        else:
            await websocket.send_text(f"Fraud type '{fraud_type}' not found")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

# 서비스 프롬프트 업데이트
@router.websocket("/ws/update_prompt")
async def update_prompt(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        prompt = db.query(ServicePrompt).first()
        if prompt:
            prompt.prompt = data.get("prompt")
        else:
            prompt = ServicePrompt(prompt=data.get("prompt"))
            db.add(prompt)
        db.commit()
        await websocket.send_text("Service prompt updated successfully")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

# 서비스 프롬프트 가져오기
@router.websocket("/ws/get_prompt")
async def get_prompt(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        prompt = db.query(ServicePrompt).first()
        await websocket.send_text(prompt.prompt if prompt else "No prompt set.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

# 사기 유형 목록 가져오기
@router.websocket("/ws/get_fraud_types")
async def get_fraud_types(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        fraud_types = db.query(FraudType).all()
        types_list = [fraud_type.type for fraud_type in fraud_types]
        await websocket.send_json(types_list)
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
