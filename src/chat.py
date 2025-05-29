import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from src.utils.chat_memory import get_memory, print_memory
import json

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

system_prompt = """
너는 챗봇 AI야.
조건1: 사용자와 대화하듯이 친근한 말투로 필요하다면 적절한 이모지를 사용하고, 문장은 엔터로 구분하여 사용자가 읽기 쉽게 대답해줘.
조건2: 질의는 주어지고 응답에 필요한 배경정보가 있다면 제공될거야.
조건3: 응답에 필요한 배경 정보가 없다면 정보나 관련 이미지를 찾을 수 없다는 식으로 응답해줘!
조건4: 정보를 이용하되 응답에 필요한 부분만 적절히 가공해서 대답해줘!
조건5: images에는 응답에 사용된 이미지의 id를 넣어주고 없으면 빈배열로 둬둬
조건6: 아래 형식을 지켜 코드블록 없이 json형태로 응답해줘
{{
  "reply": "여기에 자연어 응답 작성",
  "images": ["img_식별자1", "img_식별자2"]
}}
"""
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{messages}")
])

chain = prompt | llm

chatbot = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="messages",
    history_messages_key="chat_history"
)
    
def chat(user_query : str, session_id : str, data: dict | None = None) -> str:
    # data = {} 일 때 정보 없음 처리
    if isinstance(data, dict) and len(data) == 0:
        data = {
            "time": "정보 없음",
            "location": "정보 없음",
            "objects": [],
            "relations": []
        }
    # null이면 RAG x
    if data is None:
        user_prompt = f"[질문]\n{user_query}"    
    else:
        context_str = json.dumps(data, ensure_ascii=False, indent=2)
        user_prompt = f"[질문]\n{user_query}\n\n[배경 정보]\n{context_str}"
    
    print('생성된 프롬프트: ', user_prompt)

    response = chatbot.invoke(
        {"messages": user_prompt},
        config={"configurable": {"session_id": session_id}}
    )

    print("응답 결과:", response.content)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"reply": response.content, "images": []}


# 안씀
def generate_answer(user_query: str, data: dict | None = None) -> str:
    """
    자연어 쿼리를 바탕으로 LLM이 자연어 응답 생성(생성 정보 있으면 파라미터로)
    - data가 있을 경우: RAG 기반 응답
    - 빈 dict일 경우: 정보 없음 안내
    - None일 경우: RAG 없이 질의만으로 응답
    """
    answer = ''

    # data = {} 일 때
    if isinstance(data, dict) and len(data) == 0:
        data = {
            "time": "정보 없음",
            "location": "정보 없음",
            "objects": [],
            "relations": []
        }
    
    if data is None:
        user_prompt = f"[질문]\n{user_query}"    
    else:
        import json
        context_str = json.dumps(data, ensure_ascii=False, indent=2)
        user_prompt = f"[질문]\n{user_query}\n\n[배경 정보]\n{context_str}"
    
    print('생성된 프롬프트: ', user_prompt)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    
    answer = response.choices[0].message.content

    return answer

