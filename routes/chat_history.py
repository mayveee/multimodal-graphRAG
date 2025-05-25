from fastapi import APIRouter
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage, AIMessage
from src.utils.chat_memory import get_memory

router = APIRouter()

def strip_prompt_for_display(text: str) -> str:
    """
    [질문] 다음부터 [배경 정보] 전까지만 추출
    """
    if "[질문]" in text:
        text = text.split("[질문]", 1)[-1]
    if "[배경 정보]" in text:
        text = text.split("[배경 정보]", 1)[0]
    return text.strip()

@router.get("/chat-history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        memory = get_memory(session_id)
        raw_messages = memory.messages

        messages = []
        for msg in raw_messages:
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": strip_prompt_for_display(msg.content)})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})

        return JSONResponse(content={"messages": messages})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
