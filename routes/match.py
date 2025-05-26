# routes/match.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from src.chat import chat
import src.neo4j_runner as db
from src.dbquery_generator import generate_match_query
from src.userquery_handler import is_rag_needed

router = APIRouter()

class MessageInput(BaseModel):
    message: str

@router.post("/match")
async def match_message(input: MessageInput):
    user_message = input.message
    print("📨 사용자 메시지:", user_message)
    
    # RAG 여부 검사
    if(is_rag_needed(user_message)):
        # match query 생성
        match_query = generate_match_query(user_message)
        print('결과 쿼리: ', match_query)
        # match query 실행
        records, summary = db.run_query(match_query)
        # 질의, 결과로 응답 생성
        answer = chat(user_query=user_message, session_id="1234", data=records)
    else:
        # RAG 필요없으면 그냥 응답
        answer = chat(user_message, "1234")

    return JSONResponse(content=answer)
