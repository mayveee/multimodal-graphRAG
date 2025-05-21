from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

user_memory_store = {}

def get_memory(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in user_memory_store:
        user_memory_store[session_id] = InMemoryChatMessageHistory()
    return user_memory_store[session_id]

def print_memory(session_id: str):
    memory = get_memory(session_id)
    print(f"[{session_id}] 대화 기록:")
    for msg in memory.messages:
        if isinstance(msg, HumanMessage):
            role =  "👤 사용자"
        elif isinstance(msg, AIMessage):
            role = "🤖 챗봇"
        print(f"{role}: {msg.content}")
